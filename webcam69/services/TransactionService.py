from uuid import UUID
from dao import TransactionDAO
from models import TransactionModel
from enums import TransactionStatusEnum
from utils.AppMiddleware import HandleError


class TransactionService:
    def __init__(self, transaction_dao: TransactionDAO):
        self._transaction_dao = transaction_dao

    async def create(
            self,
            transaction_type: str,
            owner_wallet_id: UUID,
            product_id: UUID,
            total_token_price: int,
            status: str = None,
            session=None
    ) -> TransactionModel:
        transaction = await self._transaction_dao.create(
            transaction_type=transaction_type,
            owner_wallet_id=owner_wallet_id,
            product_id=product_id,
            total_token_price=total_token_price,
            status=status,
            session=session
        )

        return transaction

    async def update(self, transaction_id: UUID, status: str, session=None) -> TransactionModel:
        transaction = await self.get_by_id(transaction_id=transaction_id)

        if transaction.status == (
                TransactionStatusEnum.COMPLETED or TransactionStatusEnum.REJECTED):
            raise HandleError('Transaction is closed, you can`t change anything')

        transaction = await self._transaction_dao.update(
            transaction_id=transaction_id, status=status, session=session
        )

        return transaction

    async def get_by_id(self, transaction_id: UUID) -> TransactionModel:
        transaction = await self._transaction_dao.get_by_id(transaction_id=transaction_id)

        return transaction
