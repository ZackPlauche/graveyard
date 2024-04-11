import time
from datetime import datetime, timedelta

from elements import Element, Selector
from selenium.common.exceptions import NoSuchElementException

from wyzantapi.constants import BASE_URL, WYZANT_MIN_MESSAGE_CHARS
from wyzantapi.models import Job, Student, Application
from wyzantapi.utils import clean_text, pad_message


class JobCard(Element):
    selector = Selector(by='css selector', value='.academy-card')

    def get_data(self):
        self.show_details()
        soup = self.soup
        details = self._get_details()
        recommended_rate_str = soup.select_one('span.text-semibold.text-underscore').text.strip('\n').strip().split(': ')[-1]
        recommended_rate = int(recommended_rate_str.strip('$').strip('/hr')) if '$' in recommended_rate_str else None
        posted_at_str = soup.select_one('span.text-semibold.text-light').text.strip()
        posted_at = self._parse_posted_at(posted_at_str)
        return Job(
            id=self.url.split('/')[-1],
            url=self.url,
            found_at=datetime.now(),
            posted_at=posted_at,
            topic=soup.find('a', class_='job-details-link').text,
            description=clean_text(soup.find('p', class_='job-description').text),
            subject=details.get('Subject'),
            recommended_rate=recommended_rate,
            student=Student(
                name=soup.find('p').text,
                timezone=details.get('Timezone'),
                grade_level=details.get('Student grade level')
            ),
        )

    def show_details(self):
        """Click the 'Show Details' button on the job card to reveal more data."""
        try:
            self.find_element('css selector', '.collapsable-label').click()
            time.sleep(1)
        except NoSuchElementException:
            pass  # Sometimes cards don't have any details.

    @property
    def url(self) -> str:
        return self._get_url()

    def _get_details(self) -> dict[str, str]:
        details = {}
        detail_elements = self.soup.find_all('p', class_='spc-zero')
        for detail_element in detail_elements:
            key: str = detail_element.find('span', class_='text-light').text.strip().strip(':')
            if key == 'Availability':
                continue
            value: str = detail_element.find('span', class_='text-semibold').text
            details[key] = value
        return details

    def _get_url(self) -> str:
        return BASE_URL + self.soup.find('a', class_='job-details-link').get('href')

    def _parse_posted_at(self, posted_at_str: str) -> datetime:
            """Parse Wyzant time string into datetime object"""
            posted_at_str = posted_at_str.strip()
            now = datetime.now()
            time_char_map = {
                'm': 'minutes',
                'h': 'hours',
                'd': 'days'
            }
            if any(posted_at_str.endswith(char) for char in time_char_map.keys()):
                time_char = posted_at_str[-1]
                time_unit = time_char_map[time_char]
                time_value = int(posted_at_str[:-1])
                posted_at = now - timedelta(**{time_unit: time_value})
            else:  
                posted_at = datetime.strptime(posted_at_str, '%b %d').replace(year=now.year) # Jan 1, Feb 2, Mar 3, etc.
            return posted_at

class JobApplicationForm(Element):
    selector = Selector(by='id', value='job_application_form')

    def apply(self, message: str, rate: float | None = None) -> Application:
        """Apply to a job."""
        self.write_message(message)
        rate = self.handle_rate(rate)
        self.handle_partner_agreement_checkbox()
        self.click_submit()
        return Application(message=message, rate=rate, sent_at=datetime.now())

    def write_message(self, message: str):
        """Write a message on the application form."""
        message_input = self.find_element('id', 'personal_message')
        message_input.clear()
        message_input.send_keys_with_emojis(pad_message(message, WYZANT_MIN_MESSAGE_CHARS))

    def handle_rate(self, rate: int | None) -> float:
        """Handle the rate input on the application form."""
        try:
            if rate:
                self.update_rate(rate)
            else:
                rate = float(self.soup.find('input', id='hourly_rate').get('value'))
        except NoSuchElementException:
            try:
                rate = self._get_partner_rate_optional()
            except NoSuchElementException:
                try:
                    rate = self._get_partner_rate_required()
                except NoSuchElementException as e:
                    raise e
        except AttributeError:
            try:
                rate = self._get_partner_rate_optional()
            except NoSuchElementException as e:
                raise e
        return rate

    def _get_partner_rate_optional(self) -> float:
        rate_str = self.find_element('css selector', '.partner-rate-optional p').get_attribute('innerText')
        rate = float(rate_str.strip('$').strip('/hr'))
        return rate

    def _get_partner_rate_required(self):
        rate_str: str = self.find_element('css selector', '.partner-rate-required p').get_attribute('innerText')
        rate = float(rate_str.strip('$').strip('/hr'))
        return rate
    
    def handle_partner_agreement_checkbox(self):
        """Handle the occasional partner agreement checkbox that pops up sometimes application forms."""
        try:
            partner_agreement_checkbox = self.find_element('id', 'agree_partner_hourly_rate')
            partner_agreement_checkbox.click()
        except NoSuchElementException:
            pass

    def update_rate(self, rate: float):
        """Update the rate on the application form."""
        hourly_rate_input = self.find_element('id', 'hourly_rate')
        hourly_rate_input.clear()
        hourly_rate_input.send_keys(str(rate))


    def click_submit(self):
        """Click the submit button on the application form."""
        submit_button = self.find_element('css selector', 'input[type="submit"]')
        submit_button.click()
