from enum import Enum
from settings import Settings
from urllib.parse import urlunparse, urlparse
from os.path import join as join_path
from views import RefillTransactionDetailView


settings = Settings()


class SelfApiSpec(Enum):
    TRANSACTION_UPDATE = RefillTransactionDetailView.endpoint

    def get_url(self):
        url_parts = list(urlparse(settings.SELF_HOST))
        url_parts[2] = join_path(url_parts[2], self.value)
        url = urlunparse(url_parts)

        return url