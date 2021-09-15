from services import (
    TokenPackageService,
    TransactionService,
    TokenRateService,
    TokenWalletService,
    )
from services.products import RefillProductService
from services.sagas import PaymentSaga
from enums import TransactionStatusEnum, PaymentStatusEnum, TransactionTypeEnum
from context_managers import AtomicTransaction
from consts import DB_SESSION
from dto import TransactionRefillRequestDTO, TransactionRefillPaymentDTO, TransactionRefillPaymentRequestDTO
from models import TransactionModel
from utils.AppMiddleware import HandleError
from celery_app import celery_app


class RefillTransactionFacade:
    _match_statuses = {
        PaymentStatusEnum.PENDING.value: TransactionStatusEnum.PENDING.value,
        PaymentStatusEnum.REJECTED.value: TransactionStatusEnum.REJECTED.value,
        PaymentStatusEnum.COMPLETED.value: TransactionStatusEnum.COMPLETED.value
    }

    def __init__(
            self,
            app,
            refill_product_service: RefillProductService,
            transaction_service: TransactionService,
            token_package_service: TokenPackageService,
            token_rate_service: TokenRateService,
            token_wallet_service: TokenWalletService,
            payment_saga: PaymentSaga,
    ):
        self._app = app
        self._refill_product_service = refill_product_service
        self._payment_saga = payment_saga
        self._transaction_service = transaction_service
        self._token_package_service = token_package_service
        self._token_rate_service = token_rate_service
        self._token_wallet_service = token_wallet_service

    async def process_create(
            self, transaction_refill_request: TransactionRefillRequestDTO
    ) -> TransactionModel:
        token_price_model = await self._token_package_service.get_by_id(transaction_refill_request.token_package_id)
        fiat_price = await self._token_rate_service.get_fiat_price(
            currency=transaction_refill_request.currency,
            token_amount=token_price_model.token_price
        )

        async with AtomicTransaction(session_generator=self._app[DB_SESSION]) as session:
            try:
                product = await self._refill_product_service.create(
                    token_package_id=transaction_refill_request.token_package_id,
                    session=session
                )
                transaction = await self._transaction_service.create(
                    transaction_type=TransactionTypeEnum.REFILL.value,
                    owner_wallet_id=transaction_refill_request.owner_wallet_id,
                    product_id=product.id,
                    total_token_price=token_price_model.token_price,
                    session=session
                )
            except:
                await session.rollback()
                raise HandleError('Internal error!')

        payment_request = TransactionRefillPaymentRequestDTO(
            transaction_id=transaction.id,
            wallet_id=transaction_refill_request.owner_wallet_id,
            product_id=product.id,
            sum=fiat_price
        )

        payment_response = await self._payment_saga.create_payment(dto=payment_request)

        if payment_response.transaction_id != transaction.id:
            raise HandleError('Unexpected transaction ID')

        transaction = await self.process_update(payment_dto=payment_response)

        return transaction

    async def process_update(
            self,
            payment_dto: TransactionRefillPaymentDTO,
    ) -> TransactionModel:

        new_transaction_status = self._match_statuses.get(payment_dto.status)

        if new_transaction_status != TransactionStatusEnum.PENDING.value:
            celery_app.control.revoke(payment_dto.transaction_id)

        if new_transaction_status == TransactionStatusEnum.COMPLETED.value:
            transaction = await self._complete_transaction(
                payment_dto=payment_dto
            )
            return transaction

        transaction = await self._transaction_service.update(
            transaction_id=payment_dto.transaction_id,
            status=new_transaction_status,
        )
        await self._refill_product_service.update(
            refill_product_id=transaction.product_id,
            payment_id=payment_dto.payment_id
        )

        return transaction

    async def _complete_transaction(
            self,
            payment_dto: TransactionRefillPaymentDTO
    ) -> TransactionModel:

        async with AtomicTransaction(session_generator=self._app[DB_SESSION]) as session:
            try:
                transaction = await self._transaction_service.update(
                    transaction_id=payment_dto.transaction_id,
                    status=TransactionStatusEnum.COMPLETED.value,
                    session=session
                )
                await self._token_wallet_service.refill_wallet(
                    wallet_id=transaction.owner_wallet_id,
                    sum=transaction.product.token_package.token_amount,
                    session=session
                )
            except:
                await session.rollback()
                transaction = await self._transaction_service.update(
                    transaction_id=payment_dto.transaction_id,
                    status=TransactionStatusEnum.TRANSACTION_FAILED.value
                )
                return transaction

        return transaction

    async def reject_transaction(self, transaction_id):
        dto = TransactionRefillPaymentDTO(
            transaction_id=transaction_id,
            status=PaymentStatusEnum.REJECTED.value
        )
        await self.process_update(dto)
