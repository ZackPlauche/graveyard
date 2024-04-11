from pages import Page, DetailPage

from wyzantapi.elements import JobCard, JobApplicationForm
from wyzantapi.models import Job, Application


class JobListPage(Page):
    url = 'https://www.wyzant.com/tutor/jobs'

    def get_job_count(self):
        soup = self.soup
        return int(soup.select_one('h2 span').text)

    def get_jobs(self) -> list[Job]:
        job_cards = JobCard.find_all(self.driver)
        jobs = [job_card.get_data() for job_card in job_cards]
        return jobs



class JobDetailPage(DetailPage):
    model = Job

    def apply(self, message: str, rate=None) -> Application:
        return JobApplicationForm.find(driver=self.driver).apply(message, rate)

    def get_payment_info_on_file(self) -> bool:
        soup = self.soup
        card_icon = soup.select_one('i.wc-credit-card')
        icon_classes = card_icon.get('class')
        if 'wc-green' in icon_classes:
            return True
        elif 'wc-yellow' in icon_classes:
            return False
        else:
            raise ValueError(f'Unexpected icon classes: {icon_classes}')
