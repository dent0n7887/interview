from pydantic import BaseModel, validator
from uuid import UUID
from enums import PaymentStatusEnum
from typing import Union, Optional


class TransactionRefillRequestDTO(BaseModel):
    owner_wallet_id: Union[str, UUID]
    token_package_id: int
    currency: str

    @validator('owner_wallet_id')
    def change_types(cls, item):
        item = UUID(item)
        return item


class TransactionRefillPaymentDTO(BaseModel):
    transaction_id: Union[str, UUID]
    status: str
    payment_id: Optional[str]

    @validator('status')
    def validate_status(cls, item):
        if item not in PaymentStatusEnum.get_all():
            raise ValueError('Wrong status')
        return item

    @validator('transaction_id')
    def change_types(cls, item):
        item = UUID(item)
        return item


class TransactionRefillPaymentRequestDTO(BaseModel):
    transaction_id: UUID
    wallet_id: UUID
    product_id: UUID
    sum: float

    @validator('transaction_id', 'wallet_id', 'product_id')
    def change_types_for_json(cls, item):
        item = str(item)
        return item
