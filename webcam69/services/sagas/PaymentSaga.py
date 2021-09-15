from clients import WebClient
from enums.api_spec import ExternalBillingApiSpec
from enums import PaymentStatusEnum
from dto import TransactionRefillPaymentDTO, TransactionRefillPaymentRequestDTO
from celery_app import check_payment_status
from settings import Settings


class PaymentSaga:
    def __init__(self, web_client: WebClient):
        self._web_client = web_client
        self._settings = Settings()

    async def create_payment(self, dto: TransactionRefillPaymentRequestDTO) -> TransactionRefillPaymentDTO:

        try:
            response = await self._web_client.post(
                url=ExternalBillingApiSpec.PAYMENT_REQUEST.get_url(),
                json=dto.dict()
            )
        except:
            response_dto = TransactionRefillPaymentDTO(
                transaction_id=dto.transaction_id,
                status=PaymentStatusEnum.REJECTED.value
            )
            return response_dto

        response_dto = TransactionRefillPaymentDTO(**response.body)

        if response_dto.status == PaymentStatusEnum.PENDING.value:
            '''
            Если вернулся статус Pending - Celery ставит задачу в очередь на актуализацию статуса транзакции
            Далее если не приходит обновление статуса - по прошествии заданного времени
            вызывается метод check_payment_status и проверяется статус оплаты, актуализируется статус транзакции
            Если статус остался Pending - транзакция закрывается со статусом Rejected
            Если же обновление статуса приходит раньше заданного времени - задача отменяется
            '''
            check_payment_status.apply_async(
                countdown=self._settings.CHECK_PAYMENT_SECONDS,
                task_id=dto.transaction_id)

        return response_dto
