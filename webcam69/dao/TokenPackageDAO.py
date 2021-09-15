from models import TokenPackageModel
from context_managers import HandleSession
from consts import DB_SESSION
from sqlalchemy import update, select
from typing import List


class TokenPackageDAO:

    def __init__(self, app):
        self._app = app

    async def create(
            self,
            name: str,
            token_amount: int,
            token_price: int,
            session=None
    ) -> TokenPackageModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            token_package = TokenPackageModel(
                name=name,
                token_price=token_price,
                token_amount=token_amount)
            session.add(token_package)

            return token_package

    async def update(self, token_package_id: int, session=None, **fields) -> TokenPackageModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            await session.execute(update(TokenPackageModel).
                                  where(TokenPackageModel.id == token_package_id).values(fields))
            await session.flush()
            token_package = await session.get(TokenPackageModel, token_package_id)

            return token_package

    async def get_by_id(self, token_package_id: int, session=None) -> TokenPackageModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:

            return await session.get(TokenPackageModel, token_package_id)

    async def get_all(self, session=None) -> List[TokenPackageModel]:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            package_model = await session.execute(select(TokenPackageModel))

            return package_model.scalars().all()
