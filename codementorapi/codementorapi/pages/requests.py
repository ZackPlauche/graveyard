from codementorapi.elements import RequestDetails, RequestCardList, RequestCard, RequestInterestForm, Chatbox
from codementorapi.models import Request

from .base import BasePage, BaseDetailPage



class OpenRequestsPage(BasePage):
    url = 'https://www.codementor.io/m/dashboard/open-requests'

    def get_request_cards(self) -> list[RequestCard]:
        return RequestCardList.find(self.driver).get_items()

    def get_loaded_open_requests(self) -> list[RequestCard]:
        return RequestCardList.find(self.driver).get_loaded_items()


class RequestDetailPage(BaseDetailPage):
    model = Request

    def get_request_details(self) -> RequestDetails:
        return RequestDetails.find(self.driver)

    def apply(self, message: str):
        request_interest_form = RequestInterestForm.find(self.driver)
        request_interest_form.send_interest_message(message)
        request_interest_form = RequestInterestForm.find(self.driver) # Page reloads after sending interest message, so need to send again.
        request_interest_form.click_message_client_button()
        Chatbox.find_by_user(self.driver, self.instance.user).send_message(message)