from dao import TokenRateDAO
from models import TokenRateModel
from dto import CreateTokenRateDTO
from typing import List


class TokenRateService:
    def __init__(self, token_rate_dao: TokenRateDAO):
        self._token_rate_dao = token_rate_dao

    async def create(self, dto: CreateTokenRateDTO) -> TokenRateModel:
        model_rate = await self._token_rate_dao.create(
            currency=dto.currency,
            rate=dto.rate
        )
        return model_rate

    async def get_by_currency(self, currency: str) -> TokenRateModel:
        model_rate = await self._token_rate_dao.get_by_currency(currency=currency)

        return model_rate

    async def get_all(self) -> List[TokenRateModel]:

        return await self._token_rate_dao.get_all()

    async def get_fiat_price(self, currency: str, token_amount: int) -> float:
        model_rate = await self.get_by_currency(currency=currency)
        fiat_price = token_amount * model_rate.rate

        return fiat_price
