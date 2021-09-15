from pydantic import BaseModel
from typing import Union
from uuid import UUID


class WalletCreateDTO(BaseModel):
    user_id: Union[str, UUID]