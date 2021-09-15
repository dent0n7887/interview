import pytest
from aiohttp import web
from asyncio import get_event_loop
from clients.dto import WebClientResponse
from clients import WebClient
from consts import SETTINGS
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from os import remove
from models import (
    BaseModel,
    TokenWalletModel,
    TokenPackageModel,
    TokenRateModel,
    TransactionModel,
    ProductRefillModel,
    ProductTipsModel
)
from dao import (
    TokenPackageDAO,
    TokenWalletDAO,
    TransactionDAO,
    TokenRateDAO
)
from dao.products import RefillProductDAO, TipsProductDAO
from facades import RefillTransactionFacade, TipsTransactionFacade
from services.sagas import PaymentSaga
from services.products import RefillProductService, TipsProductService
from services import (
    TransactionService,
    TokenWalletService,
    TokenPackageService,
    TokenRateService,
)
from settings import Settings
from dto import (
    TransactionTipsRequestDTO,
    TransactionRefillPaymentDTO,
    TransactionRefillRequestDTO,
    TransactionRefillPaymentRequestDTO
)
from consts import DB_SESSION
from utils.AppMiddleware import HandleError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


@pytest.fixture
def loop():
    return get_event_loop()


@pytest.fixture
def get_app(f_session):
    app = web.Application()
    app[DB_SESSION] = f_session
    return app


@pytest.fixture
def env_settings(env_setup, get_app):
    settings = Settings(_env_file=".env_test")
    get_app[SETTINGS] = settings
    return settings


@pytest.fixture
def env_setup(request, env_data):
    with open('.env_test', 'w') as file:
        file.writelines([f"{key} = {env_data[key]}\n" for key in env_data])

    def env_teardown():
        remove(".env_test")

    request.addfinalizer(env_teardown)


@pytest.fixture
def env_data():
    return {
        "DB_NAME": "test_db_name",
        "DB_USER": "test_db_user",
        "DB_PASSWORD": "test_db_pass",
        "DB_HOST": "test_db_host",
        "EXTERNAL_BILLING_API_URL": "http://external-billing/api/"
    }


@pytest.fixture
def f_tips_product_dao():
    return TipsProductDAO(app=get_app)


@pytest.fixture
def f_token_rate_dao():
    return TokenRateDAO(app=get_app)


@pytest.fixture
def f_refill_product_dao():
    return RefillProductDAO(app=get_app)


@pytest.fixture
def f_token_package_dao():
    return TokenPackageDAO(app=get_app)


@pytest.fixture
def f_token_wallet_dao():
    return TokenWalletDAO(app=get_app)


@pytest.fixture
def f_transaction_dao():
    return TransactionDAO(app=get_app)


@pytest.fixture
def f_web_client():
    return WebClient()


@pytest.fixture
def f_payment_saga(f_web_client):
    return PaymentSaga(web_client=f_web_client)


@pytest.fixture
def f_transaction_service(f_transaction_dao):
    return TransactionService(transaction_dao=f_transaction_dao)


@pytest.fixture
def f_token_wallet_service(f_token_wallet_dao):
    return TokenWalletService(token_wallet_dao=f_token_wallet_dao)


@pytest.fixture
def f_token_package_service(f_token_package_dao):
    return TokenPackageService(token_package_dao=f_token_package_dao)


@pytest.fixture
def f_token_rate_service(f_token_rate_dao):
    return TokenRateService(token_rate_dao=f_token_rate_dao)


@pytest.fixture
def f_refill_product_service(f_refill_product_dao):
    return RefillProductService(refill_product_dao=f_refill_product_dao)


@pytest.fixture
def f_tips_product_service(f_tips_product_dao):
    return TipsProductService(tips_product_dao=f_tips_product_dao)


@pytest.fixture
def f_refill_order_facade(
        f_token_package_service,
        f_refill_product_service,
        f_token_wallet_service,
        f_transaction_service,
        f_payment_saga,
        f_token_rate_service,
        get_app
):
    return RefillTransactionFacade(
        app=get_app,
        token_wallet_service=f_token_wallet_service,
        transaction_service=f_transaction_service,
        refill_product_service=f_refill_product_service,
        token_package_service=f_token_package_service,
        token_rate_service=f_token_rate_service,
        payment_saga=f_payment_saga
    )


@pytest.fixture
def f_tips_transaction_facade(
        f_transaction_service,
        f_token_wallet_service,
        f_tips_product_service
):
    return TipsTransactionFacade(
        app=get_app,
        transaction_service=f_transaction_service,
        token_wallet_service=f_token_wallet_service,
        tips_product_service=f_tips_product_service
    )


@pytest.fixture
def f_transaction_refill_request_dto():
    return TransactionRefillRequestDTO(
        owner_wallet_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        token_package_id=1,
        currency='EUR'
    )


@pytest.fixture
def f_transaction_refill_payment_request_dto():
    return TransactionRefillPaymentRequestDTO(
        wallet_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        product_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        sum=3.99
    )


@pytest.fixture
def f_saga_payment_response():
    return WebClientResponse(
        body={
            "transaction_id": "c402f056-9a85-4137-8b84-0e2657d0dd0a",
            "status": "COMPLETED",
            "payment_id": "c402f056-9a85-4137-8b84-0e2657d0dd0a"
        }
    )


@pytest.fixture
def f_transaction_refill_payment_dto_complete():
    return TransactionRefillPaymentDTO(
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        status='COMPLETED',
        payment_id='c402f056-9a85-4137-8b84-0e2657d0dd0a'
    )


@pytest.fixture
def f_transaction_refill_payment_dto_pending():
    return TransactionRefillPaymentDTO(
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        status='PENDING',
        payment_id='c402f056-9a85-4137-8b84-0e2657d0dd0a'
    )


@pytest.fixture
def f_transaction_refill_payment_dto_reject():
    return TransactionRefillPaymentDTO(
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        status='REJECTED'
    )


@pytest.fixture
def f_transaction_model_complete(f_product_refill_model):
    transaction = TransactionModel(
        id=UUID('c402f056-9a85-4137-8b84-0e2657d0dd0a'),
        transaction_type='REFILL',
        owner_wallet_id='8376109d-9241-4200-9ed9-7b8e81114ea5',
        product_id='8376109d-9241-4200-9ed9-7b8e81114ea5',
        total_token_price=20,
        status='COMPLETED'
    )
    setattr(transaction, 'product', f_product_refill_model)

    return transaction


@pytest.fixture
def f_transaction_model_pending():
    return TransactionModel(
        id=UUID('c402f056-9a85-4137-8b84-0e2657d0dd0a'),
        transaction_type='REFILL',
        owner_wallet_id='8376109d-9241-4200-9ed9-7b8e81114ea5',
        product_id='8376109d-9241-4200-9ed9-7b8e81114ea5',
        total_token_price=20,
        status='PENDING'
    )


@pytest.fixture
def f_transaction_refill_payment_dto_pending():
    return TransactionRefillPaymentDTO(
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        status='PENDING'
    )


@pytest.fixture
def f_transaction_refill_payment_dto_completed():
    return TransactionRefillPaymentDTO(
        transaction_id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        status='COMPLETED',
        payment_id='c402f056-9a85-4137-8b84-0e2657d0dd0a'
    )


@pytest.fixture
def f_token_package_model():
    return TokenPackageModel(
        id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        name='big',
        token_amount=20,
        token_price=20
    )


@pytest.fixture
def f_product_refill_model(f_token_package_model):
    product = ProductRefillModel(
        id='c402f056-9a85-4137-8b84-0e2657d0dd0a',
        token_package_id=1,
        payment_id='c402f056-9a85-4137-8b84-0e2657d0dd0a'
    )
    setattr(product, 'token_package', f_token_package_model)

    return product


@pytest.fixture
def f_token_rate_model():
    return TokenRateModel(
        id=1,
        currency='EUR',
        rate=1
    )


@pytest.fixture
def f_session():
    return sessionmaker(
        create_async_engine('postgresql+asyncpg://TEST:TEST@127.0.0.1/TEST'),
        class_=AsyncSession
    )