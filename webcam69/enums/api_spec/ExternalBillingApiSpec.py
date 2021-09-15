from enum import Enum
from settings import Settings
from urllib.parse import urlunparse, urlparse
from os.path import join as join_path


settings = Settings()


class ExternalBillingApiSpec(Enum):
    PAYMENT_REQUEST = 'payment'
    GET_PAYMENT = 'payment?transaction_id={transaction_id}'

    def get_url(self):
        url_parts = list(urlparse(settings.EXTERNAL_BILLING_API_URL))
        url_parts[2] = join_path(url_parts[2], self.value)
        url = urlunparse(url_parts)

        return url