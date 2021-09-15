from enum import Enum
from typing import List


class TransactionTypeEnum(Enum):

    TIPS = "TIPS"
#    PURCHASE = "PURCHASE
    REFILL = "REFILL"

    @classmethod
    def get_all(cls) -> List[str]:
        return [t.value for t in cls]