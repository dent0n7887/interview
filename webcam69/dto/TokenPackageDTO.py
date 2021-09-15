from pydantic import BaseModel


class CreateTokenPackageDTO(BaseModel):
    name: str
    token_amount: int
    token_price: int