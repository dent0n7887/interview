from pydantic import BaseModel, validator
from utils.AppMiddleware import HandleError


class CreateTokenRateDTO(BaseModel):
    currency: str
    rate: float

    @validator('currency')
    def validate_currency(cls, item):
        if len(item) > 5:
            raise HandleError('Incorrect currency')
        return item