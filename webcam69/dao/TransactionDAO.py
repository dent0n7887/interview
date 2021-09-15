from uuid import UUID
from models import TransactionModel
from context_managers import HandleSession
from consts import DB_SESSION
from enums import TransactionTypeEnum, TransactionStatusEnum
from sqlalchemy import update


class TransactionDAO:

    def __init__(self, app):
        self._app = app

    async def create(
            self,
            transaction_type: str or TransactionTypeEnum,
            owner_wallet_id: UUID,
            product_id: UUID,
            total_token_price: int,
            status: str or TransactionStatusEnum,
            session=None
    ) -> TransactionModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            transaction = TransactionModel(
                transaction_type=transaction_type,
                owner_wallet_id=owner_wallet_id,
                product_id=product_id,
                total_token_price=total_token_price,
                status=status
            )
        session.add(transaction)
        await session.flush()
        await session.refresh(transaction)

        return transaction

    async def update(
            self, transaction_id: UUID, status: str or TransactionTypeEnum, session=None
    ) -> TransactionModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            transaction = await session.execute(
                update(TransactionModel).
                    where(TransactionModel.id == transaction_id).
                    values(status=status)
            )
            await session.flush()
            transaction = await session.get(TransactionModel, transaction_id)

            return transaction

    async def get_by_id(self, transaction_id: UUID, session=None) -> TransactionModel:
        async with HandleSession(session_generator=self._app[DB_SESSION], session=session) as session:
            return await session.get(TransactionModel, transaction_id)
