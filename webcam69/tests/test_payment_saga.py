import pytest
from enums.api_spec import ExternalBillingApiSpec
from mockito import when
from tests import conftest


@pytest.mark.asyncio
async def test_payment_saga_success(
        httpserver,
        f_saga_payment_response,
        f_payment_saga,
        f_transaction_refill_payment_request_dto,
        f_transaction_refill_payment_dto_complete
):
    when(conftest.ExternalBillingApiSpec).get_url(...). \
        thenReturn(httpserver.url_for('') + '/api/' + ExternalBillingApiSpec.PAYMENT_REQUEST.value)
    httpserver.expect_request(method="POST", uri='/api/' + ExternalBillingApiSpec.PAYMENT_REQUEST.value). \
        respond_with_json(f_saga_payment_response.body)
    dto = await f_payment_saga.create_payment(f_transaction_refill_payment_request_dto)

    assert dto.dict() == f_transaction_refill_payment_dto_complete.dict()


@pytest.mark.asyncio
async def test_payment_saga_fail(
        f_payment_saga,
        f_transaction_refill_payment_request_dto,
        f_transaction_refill_payment_dto_reject
):
    dto = await f_payment_saga.create_payment(f_transaction_refill_payment_request_dto)

    assert dto.dict() == f_transaction_refill_payment_dto_reject.dict()
