import os
import time
from pathlib import Path
from datetime import datetime, date, timedelta

import pandas as pd
from bs4 import BeautifulSoup, Tag
from selenium import webdriver

from driver import start_driver, safe_get
from messages import (
    CAN_HELP_MESSAGE,
    UNABLE_TO_HELP_MESSAGE,
    OLD_JOB_MESSAGE,
    pad_message,
)

pd.options.mode.chained_assignment = None  # default='warn'


WYZANT_URL = 'https://www.wyzant.com'

JOBS_URL = WYZANT_URL + '/tutor/jobs'

FILTER_WORDS = [
    'react',
    'reactjs',
    'angular',
    'machine learning',
    'deep learning',
]

JOB_INFO_TEMPLATE = """\
Client: {client_name}
Subject: {subject}
Description: {description}
Date Published: {date_published}\
"""

JOB_MESSAGE_MAP = {
    'Can Help': CAN_HELP_MESSAGE,
    'Unable to Help': UNABLE_TO_HELP_MESSAGE,
    'Old Job': OLD_JOB_MESSAGE,
}

TEST_MODE = False

# Paths
DATA_FOLDER = Path('data')
DATA_FOLDER.mkdir(exist_ok=True)
JOBS_CSV_PATH = DATA_FOLDER / 'jobs.csv'
JOBS_TEST_CSV_PATH = DATA_FOLDER / 'jobs_test.csv'


def main():
    # Collect all jobs from all job list pages
    # 1. Start the driver
    driver = start_driver()
    try:
        jobs_df = scrape_jobs_from_wyzant(driver)
    except:
        print('No jobs available.')
        os.system('pause')
    if len(jobs_df) and JOBS_CSV_PATH.exists():
        old_df = read_jobs()
        jobs_df = pd.concat([old_df, jobs_df], ignore_index=True)
        save_jobs(jobs_df)
        decide_job_statuses(jobs_df)
        save_jobs(jobs_df)
        send_messages(jobs_df, driver)
        save_jobs(jobs_df)
        return driver
    else:
        print('No jobs found.')
        os.system('pause')


def save_jobs(jobs_df: pd.DataFrame):
    """Save jobs DataFrame to CSV"""
    if TEST_MODE:
        jobs_df.to_csv(JOBS_TEST_CSV_PATH, index=False)
    else:
        jobs_df.to_csv(JOBS_CSV_PATH, index=False)


def scrape_jobs_from_wyzant(driver: webdriver.Chrome) -> list[dict]:
    """Collect all active jobs datum from all job list pages"""
    pages = get_page_count(driver)
    job_list = []
    for page_number in range(1, pages + 1): 
        safe_get(f'{JOBS_URL}?page={page_number}', driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.find_all('div', class_='academy-card')
        job_list.extend(parse_job_from_card(card) for card in job_cards)
    jobs_df = build_jobs_df(job_list)
    return jobs_df


def get_page_count(driver: webdriver.Chrome) -> int:
    """Get number of pages of jobs"""
    safe_get(WYZANT_URL + '/tutor/jobs', driver)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    available_jobs = int(soup.select_one('h2 > span').text)
    pages = available_jobs // 10 + 1
    return pages


def build_jobs_df(job_list: list[dict]) -> pd.DataFrame:
    """Build jobs DataFrame from list of job datum dictionaries"""
    jobs_df = pd.DataFrame(job_list)
    jobs_df['description'] = jobs_df['description'].str.replace('\n', ' ').str.replace('’', "'")
    jobs_df['date_published'] = pd.to_datetime(jobs_df['date_published']).dt.date
    jobs_df['payment_info'] = None
    jobs_df['message'] = None
    jobs_df['message_sent'] = False
    jobs_df['message_sent_date'] = None
    jobs_df['message_sent_time'] = None
    jobs_df['status'] = None
    return jobs_df


def parse_job_from_card(job_card: Tag) -> dict:
    """Parse job from job card"""
    soup = BeautifulSoup(str(job_card), 'html.parser')
    url = WYZANT_URL + soup.find('a', class_='job-details-link')['href']
    subject = soup.find('a', class_='job-details-link').text
    description = soup.find('p', class_='job-description').text
    client_name = soup.select_one('p.text-semibold.spc-zero-n.spc-tiny-s').text.strip()
    date_published = parse_wyzant_job_date(soup.select_one('div.pull-right.small-hide > span.text-semibold.text-light').text)
    return {
        'url': url,
        'subject': subject,
        'description': description,
        'client_name': client_name,
        'date_published': date_published,
    }


def parse_wyzant_job_date(date_string: str) -> date:
    """Parse Wyzant time string into datetime object"""
    date_string = date_string.strip()
    if date_string.endswith('m'):  # 10m, 20m, 30m, etc.
        return (datetime.now() - timedelta(minutes=int(date_string[:-1]))).date()
    if date_string.endswith('h'):  # 2h, 3h, 4h, etc.
        return (datetime.now() - timedelta(hours=int(date_string[:-1]))).date()
    elif date_string.endswith('d'):  # 2d, 3d, 4d, etc.
        return (datetime.now() - timedelta(days=int(date_string[:-1]))).date()
    else:  # Jan 1, Feb 2, Mar 3, etc.
        dt = datetime.strptime(date_string, '%b %d')
        dt = dt.replace(year=datetime.now().year)
        return dt.date()


def decide_job_statuses(jobs_df: pd.DataFrame):
    """Decide which jobs you can help with"""
    no_status_jobs = jobs_df[jobs_df['status'].isnull()]
    # 1. If job is old, mark as 'Old Job'
    no_status_jobs.loc[jobs_df['date_published'].apply(job_is_old), 'status'] = 'Old Job'
    # 2. If job's description contains any word in filter words, mark as 'Unable to Help'
    no_status_jobs.loc[jobs_df['description'].str.lower().str.contains('|'.join(FILTER_WORDS)), 'status'] = 'Unable to Help'
    # 3. Manually decide which jobs you can help with via Input
    new_status_jobs = no_status_jobs[no_status_jobs['status'].notnull()]
    print(f'{len(new_status_jobs)} automatically decided!')
    for i, row in new_status_jobs.iterrows():
        print(JOB_INFO_TEMPLATE.format(**row))
        print(row['status'], end='\n\n')
    still_no_status_jobs = no_status_jobs[no_status_jobs['status'].isnull()]
    print(f'{len(still_no_status_jobs)} remaining.', end='\n\n')
    for i, (index, row) in enumerate(still_no_status_jobs.iterrows(), 1):
        print(f'Job {i} of {len(still_no_status_jobs)}', end='\n\n')
        print(JOB_INFO_TEMPLATE.format(**row), end='\n\n')
        can_help = input('Can you help with this job? (y/n): ')
        if can_help.lower() == 'y':
            still_no_status_jobs.loc[index, 'status'] = 'Can Help'
        else:
            still_no_status_jobs.loc[index, 'status'] = 'Unable to Help'
        print()  # Add a newline for readability
    no_status_jobs.update(still_no_status_jobs)
    jobs_df.update(no_status_jobs)
    


def job_is_old(publised_date: date):
    """Return True if job is old"""
    return publised_date < (datetime.now() - timedelta(days=7)).date()


def send_messages(jobs_df: pd.DataFrame, driver: webdriver.Chrome):
    """Send a message to all jobs that haven't had a message sent yet."""
    unsent_jobs_df = jobs_df[jobs_df['message_sent'] == False]
    for i, (index, row) in enumerate(unsent_jobs_df.iterrows(), 1):
        print(f'Sending message to job {i} of {len(unsent_jobs_df)}', end='\n\n')
        safe_get(row['url'], driver)
        message = pad_message(JOB_MESSAGE_MAP[row['status']].format(**row))
        message_texarea = driver.find_element('id', 'personal_message')
        driver.execute_script("arguments[0].value += arguments[1]", message_texarea, message)
        # Click 'Agree to hourly rate' checkbox if it exists
        try:
            driver.find_element('css selector', '#agree_partner_hourly_rate').click()
        except:
            pass
        driver.find_element('css selector', '#job_application_form > input.btn.old-button-color').click()
        unsent_jobs_df.loc[index, 'message'] = message 
        unsent_jobs_df.loc[index, 'message_sent'] = True
        unsent_jobs_df.loc[index, 'message_sent_date'] = datetime.now().date()
        unsent_jobs_df.loc[index, 'message_sent_time'] = datetime.now().time()
        print('Message sent!', end='\n\n')
        time.sleep(2)  # Wait 2 seconds before sending next message (to avoid spamming)
    jobs_df.update(unsent_jobs_df)



def read_jobs() -> pd.DataFrame:
    """Read jobs from csv file"""
    jobs_df = pd.read_csv(DATA_FOLDER / 'jobs.csv')
    jobs_df['date_published'] = pd.to_datetime(jobs_df['date_published']).dt.date
    return jobs_df


def merge_jobs_csv_with_test_csv():
    """Merge jobs.csv with test_jobs.csv"""
    jobs_df = read_jobs()
    test_jobs_df = pd.read_csv(DATA_FOLDER / 'test_jobs.csv')
    pd.merge(jobs_df, test_jobs_df, how='outer').to_csv(DATA_FOLDER / 'jobs.csv', index=False)


if __name__ == '__main__':
    driver = main()

