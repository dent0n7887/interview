from enum import Enum
from typing import List


class TransactionStatusEnum(Enum):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'
    TRANSACTION_FAILED = 'TRANSACTION_FAILED'

    @classmethod
    def get_all(cls) -> List[str]:
        return [t.value for t in cls]