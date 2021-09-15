from services import TransactionService, TokenWalletService
from services.products import TipsProductService
from dto import TransactionTipsRequestDTO
from models import TransactionModel
from context_managers import AtomicTransaction
from consts import DB_SESSION
from enums import TransactionTypeEnum, TransactionStatusEnum
from utils.AppMiddleware import HandleError, HandleDBError


class TipsTransactionFacade:
    def __init__(
            self,
            app,
            transaction_service: TransactionService,
            token_wallet_service: TokenWalletService,
            tips_product_service: TipsProductService
    ):
        self._app = app
        self._transaction_service = transaction_service
        self._token_wallet_service = token_wallet_service
        self._tips_product_service = tips_product_service

    async def process(self, dto: TransactionTipsRequestDTO) -> TransactionModel:
        async with AtomicTransaction(session_generator=self._app[DB_SESSION]) as session:
            try:
                product = await self._tips_product_service.create(
                    recipient_wallet_id=dto.recipient_wallet_id,
                    session=session
                )
                transaction = await self._transaction_service.create(
                    transaction_type=TransactionTypeEnum.TIPS.value,
                    owner_wallet_id=dto.owner_wallet_id,
                    product_id=product.id,
                    total_token_price=dto.sum,
                    status=TransactionStatusEnum.COMPLETED.value,
                    session=session
                )
                await self._token_wallet_service.transfer(
                    wallet_id=dto.owner_wallet_id,
                    recipient_wallet_id=dto.recipient_wallet_id,
                    sum=dto.sum,
                    session=session
                )
            except HandleDBError as err:
                await session.rollback()
                raise err
            except:
                await session.rollback()
                raise HandleError('Transaction failed')

        return transaction
