from enum import Enum
from typing import List


class OrderTypeToServiceEnum(Enum):

    TRANSFER = 'TRANSFER_ORDER_FACADE'
    PRIVATE = 'PRIVATE_ORDER_FACADE'
    STATUS = 'STATUS_ORDER_FACADE'


    @classmethod
    def get_all(cls) -> List[str]:
        return [t.value for t in cls]


