from celery import Celery
from enums.api_spec import ExternalBillingApiSpec, SelfApiSpec
from enums import PaymentStatusEnum
from dto import TransactionRefillPaymentDTO
from settings import Settings
import requests

settings = Settings()
celery_app = Celery('schedule', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')


class CeleryTasks():

    def check_payment(self, transaction_id):
        external_billing_url = ExternalBillingApiSpec.GET_PAYMENT.get_url()
        transaction_update_url = SelfApiSpec.TRANSACTION_UPDATE.get_url()
        try:
            response = requests.get(external_billing_url.format(transaction_id=transaction_id))
        except:
            requests.patch(
                transaction_update_url.format(transaction_id=transaction_id),
                json={'status': PaymentStatusEnum.REJECTED.value}
            )
            return

        response_dto = TransactionRefillPaymentDTO(**response.json())

        if response_dto.status == PaymentStatusEnum.PENDING.value:
            requests.patch(
                transaction_update_url.format(transaction_id=transaction_id),
                json={'status': PaymentStatusEnum.REJECTED.value}
            )
            return

        requests.patch(
            transaction_update_url.format(transaction_id=transaction_id),
            json=response_dto.dict(exclude={'transaction_id'})
        )
        return


celery_tasks = CeleryTasks()


@celery_app.task(bind=True)
def check_payment_status(self):
    celery_tasks.check_payment(transaction_id=self.request.id)
