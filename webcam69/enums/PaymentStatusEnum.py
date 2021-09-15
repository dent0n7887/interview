from enum import Enum
from typing import List


class PaymentStatusEnum(Enum):
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'

    @classmethod
    def get_all(cls) -> List[str]:
        return [t.value for t in cls]