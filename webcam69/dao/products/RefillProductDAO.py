from uuid import UUID
from models import ProductRefillModel
from context_managers import HandleSession
from consts import DB_SESSION
from sqlalchemy import update


class RefillProductDAO:
    def __init__(self, app):
        self._app = app

    async def create(self, token_package_id: int, session=None) -> ProductRefillModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            product = ProductRefillModel(
                token_package_id=token_package_id,
            )
            session.add(product)
            await session.flush()
            await session.refresh(product)

            return product

    async def update(self, refill_product_id: UUID, session=None, **fields) -> ProductRefillModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            await session.execute(
                update(ProductRefillModel).
                    where(ProductRefillModel.id == refill_product_id).
                    values(fields)
            )

            await session.flush()
            product = await session.get(ProductRefillModel, refill_product_id)

            return product

    async def get_by_id(self, refill_product_id: UUID, session=None) -> ProductRefillModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            return await session.get(ProductRefillModel, refill_product_id)