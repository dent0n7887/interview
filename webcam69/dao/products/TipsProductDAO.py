from uuid import UUID
from models import ProductTipsModel
from context_managers import HandleSession
from consts import DB_SESSION


class TipsProductDAO:
    def __init__(self, app):
        self._app = app

    async def create(self, recipient_wallet_id: UUID, session=None) -> ProductTipsModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            product = ProductTipsModel(
                recipient_wallet_id=recipient_wallet_id,
            )
            session.add(product)
            await session.flush()
            await session.refresh(product)

            return product

    async def get_by_id(self, tips_product_id: UUID, session=None) -> ProductTipsModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            return await session.get(ProductTipsModel, tips_product_id)