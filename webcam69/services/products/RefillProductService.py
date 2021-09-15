from dao.products import RefillProductDAO
from uuid import UUID
from models import ProductRefillModel


class RefillProductService:

    def __init__(
            self,
            refill_product_dao: RefillProductDAO,
    ):
        self._refill_product_dao = refill_product_dao

    async def create(self, token_package_id: int, session=None) -> ProductRefillModel:
        product = await self._refill_product_dao.create(
            token_package_id=token_package_id,
            session=session
        )
        return product

    async def update(self, refill_product_id: UUID, payment_id: str or UUID) -> ProductRefillModel:
        product = await self._refill_product_dao.update(
            refill_product_id=refill_product_id,
            payment_id=payment_id
        )
        return product

    async def get_by_id(self, refill_product_id: UUID) -> ProductRefillModel:
        product = await self._refill_product_dao.get_by_id(refill_product_id=refill_product_id)
        return product
