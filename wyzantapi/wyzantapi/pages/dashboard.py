from pages import Page


class Dashboard(Page):
    url = 'https://www.wyzant.com/tutor/home'
    load_time = 10

    def get_job_count(self) -> int:
        job_count_str = self.driver.find_element('css selector', '#jobs-widget > a > div > div > h3').get_attribute('innerText')
        job_count = int(job_count_str.split()[0])
        return job_count

