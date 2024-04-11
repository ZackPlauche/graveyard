import os

from square.client import Client as SquareClient
from square.api.invoices_api import InvoicesApi


class SquareAPI(SquareClient):

    def __init__(self, access_token: str, environment: str, location_id: str | None = None, **kwargs):
        """Create a SquareAPI instance."""
        super().__init__(access_token=access_token, environment=environment, **kwargs)
        self.location_id = location_id
        self.invoices: InvoicesApi = self.invoices


    @classmethod
    def from_env(cls, **kwargs):
        """Create a SquareAPI instance from environment variables."""
        return cls(
            access_token=os.getenv('SQUARE_ACCESS_TOKEN'),
            environment=os.getenv('SQUARE_ENVIRONMENT'),
            location_id=os.getenv('SQUARE_LOCATION_ID'),
            **kwargs)


    def get_invoices(self, location_id: str | None = None):
        """Get all invoices from a square account."""
        invoices = []
        location_id = location_id or self.location_id
        cursor = None
        while True:
            invoices_response = self.invoices.list_invoices(cursor=cursor, location_id=location_id, limit=200)
            if invoices_response.is_success():
                invoices.extend(invoices_response.body['invoices'])
                cursor = invoices_response.body.get('cursor')
                if not cursor:
                    break
            else:
                raise Exception(invoices_response.errors)
        return invoices

