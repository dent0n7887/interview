from models import TokenRateModel
from context_managers import HandleSession
from consts import DB_SESSION
from sqlalchemy import update, select
from typing import List


class TokenRateDAO:

    def __init__(self, app):
        self._app = app

    async def create(
            self,
            currency: str,
            rate: float,
            session=None
    ) -> TokenRateModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            model_token_rate = TokenRateModel(
                currency=currency,
                rate=rate)
            session.add(model_token_rate)

            return model_token_rate

    async def update(self, token_rate_id: int, rate: float, session=None) -> TokenRateModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            await session.execute(update(TokenRateModel).
                                  where(TokenRateModel.id == token_rate_id).values(rate=rate))
            await session.flush()
            model_token_rate = await session.get(TokenRateModel, token_rate_id)

            return model_token_rate

    async def get_by_currency(self, currency: str, session=None) -> TokenRateModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            model_token_rate = await session.execute(select(TokenRateModel).
                                                      filter(TokenRateModel.currency == currency))

            return model_token_rate.scalars().first()

    async def get_all(self, session=None) -> List[TokenRateModel]:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            rate_model = await session.execute(select(TokenRateModel))

            return rate_model.scalars().all()
