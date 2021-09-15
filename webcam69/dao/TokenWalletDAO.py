from consts import DB_SESSION
from models import TokenWalletModel
from sqlalchemy.future import select
from context_managers import HandleSession
from uuid import UUID
from typing import List
from utils.AppMiddleware import HandleError, HandleDBError


class TokenWalletDAO:
    def __init__(self, app):
        self._app = app

    async def create(self, user_id: UUID) -> TokenWalletModel:
        async with self._app[DB_SESSION]() as session:
            wallet = TokenWalletModel(user_id=user_id)
            session.add(wallet)
            await session.commit()

            return wallet

    async def get_by_id(self, wallet_id: UUID, session=None) -> TokenWalletModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            return await session.get(TokenWalletModel, wallet_id)

    async def get_by_user(self, user_id: UUID, session=None) -> List[TokenWalletModel]:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            wallets = await session.execute(select(TokenWalletModel).
                                           filter(TokenWalletModel.user_id == user_id))
            wallets = wallets.scalars().all()

            return wallets

    async def change_balance(self, wallet_id: UUID, sum: int, session=None) -> TokenWalletModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            try:
                wallet = await session.get(TokenWalletModel, wallet_id, with_for_update=True)
            except:
                raise HandleError('Wrong ID')

            if sum < 0 and wallet.balance + sum < 0:
                raise HandleError('Not enough money on the balance')

            wallet.balance += sum
            session.add(wallet)

            return wallet

    async def transfer(self,
                       wallet_id: UUID,
                       recipient_wallet_id: UUID,
                       sum: int,
                       session=None):
        if sum <= 0:
            raise HandleDBError('Sum must be positive')

        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            try:
                wallet = await session.get(TokenWalletModel, wallet_id, with_for_update=True)
                recipient_wallet = await session.get(
                    TokenWalletModel, recipient_wallet_id, with_for_update=True
                )
            except:
                raise HandleDBError('Wrong ID')

            if wallet.balance - sum < 0:
                raise HandleDBError('Not enough money on the balance')

            wallet.balance -= sum
            recipient_wallet.balance += sum

            session.add(wallet)
            session.add(recipient_wallet)
