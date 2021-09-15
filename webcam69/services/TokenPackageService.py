from dao import TokenPackageDAO
from models import TokenPackageModel
from dto import CreateTokenPackageDTO
from typing import List


class TokenPackageService:
    def __init__(self, token_package_dao: TokenPackageDAO):
        self._token_package_dao = token_package_dao

    async def create(self, dto: CreateTokenPackageDTO) -> TokenPackageModel:
        token_package = await self._token_package_dao.create(
            name=dto.name,
            token_price=dto.token_price,
            token_amount=dto.token_amount
        )
        return token_package

    async def get_all(self) -> List[TokenPackageModel]:

        return await self._token_package_dao.get_all()

    async def update(self, token_package_id: int, **fields) -> TokenPackageModel:
        token_package = await self._token_package_dao.update(
            token_package_id=token_package_id,
            fields=fields
        )
        return token_package

    async def get_by_id(self, token_package_id: int) -> TokenPackageModel:
        token_package = await self._token_package_dao.get_by_id(
            token_package_id=token_package_id
        )
        return token_package
