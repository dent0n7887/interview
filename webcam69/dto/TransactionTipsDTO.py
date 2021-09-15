from pydantic import BaseModel, validator
from uuid import UUID
from typing import Union


class TransactionTipsRequestDTO(BaseModel):
    owner_wallet_id: Union[str, UUID]
    recipient_wallet_id: Union[str, UUID]
    sum: int

    @validator('sum')
    def check_sum(cls, item):
        if item <= 0:
            raise ValueError('Sum must be greater then zero')
        return item

    @validator('recipient_wallet_id')
    def validate_wallets(cls, item, values):
        if item == values['owner_wallet_id']:
            raise ValueError('Wallets must be different')
        return item

    @validator('recipient_wallet_id', 'owner_wallet_id')
    def change_types(cls, item):
        item = UUID(item)
        return item