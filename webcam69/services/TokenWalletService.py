from dao.TokenWalletDAO import TokenWalletDAO
from models import TokenWalletModel
from uuid import UUID
from utils.AppMiddleware import HandleError
from dto import WalletCreateDTO
from typing import List


class TokenWalletService:
    def __init__(self, token_wallet_dao: TokenWalletDAO):
        self._token_wallet_dao = token_wallet_dao

    async def create_wallet(self, dto: WalletCreateDTO) -> TokenWalletModel:
        wallet = await self._token_wallet_dao.create(user_id=dto.user_id)
        return wallet

    async def get_by_user(self, user_id: UUID) -> List[TokenWalletModel]:
        wallets = await self._token_wallet_dao.get_by_user(user_id=user_id)
        return wallets

    async def refill_wallet(self, wallet_id: UUID, sum: int, session=None) -> TokenWalletModel:
        if sum <= 0:
            raise HandleError('sum must be positive')
        wallet = await self._token_wallet_dao.change_balance(wallet_id=wallet_id, sum=sum, session=session)
        return wallet

    async def withdrawal_wallet(self, wallet_id: UUID, sum: int, session=None) -> TokenWalletModel:
        if sum <= 0:
            raise HandleError('sum must be positive')
        wallet = await self._token_wallet_dao.change_balance(wallet_id=wallet_id, sum=-sum, session=session)
        return wallet

    async def transfer(
            self, wallet_id: UUID, recipient_wallet_id: UUID, sum: int, session=None
    ):
        if recipient_wallet_id == wallet_id:
            raise HandleError('wallets must be different')
        await self._token_wallet_dao.transfer(
            wallet_id=wallet_id,
            recipient_wallet_id=recipient_wallet_id,
            sum=sum,
            session=session
        )
