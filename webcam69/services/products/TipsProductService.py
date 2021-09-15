from dao.products import TipsProductDAO
from uuid import UUID
from models import ProductTipsModel


class TipsProductService:

    def __init__(
            self,
            tips_product_dao: TipsProductDAO,
    ):
        self._tips_product_dao = tips_product_dao

    async def create(self, recipient_wallet_id: UUID, session=None) -> ProductTipsModel:
        product = await self._tips_product_dao.create(
            recipient_wallet_id=recipient_wallet_id,
            session=session
        )
        return product

    async def get_by_id(self, tips_product_id: UUID) -> ProductTipsModel:
        product = await self._tips_product_dao.get_by_id(tips_product_id=tips_product_id)
        return product
