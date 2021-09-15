from aiohttp import web
from settings.settings import Settings
from clients import WebClient
from utils.AppMiddleware import error_middleware
from consts import (
    DB_SESSION,
    SETTINGS,
    TOKEN_PACKAGE_SERVICE,
    TOKEN_WALLET_SERVICE,
    TRANSACTION_SERVICE,
    TOKEN_RATE_SERVICE,
    REFILL_PRODUCT_SERVICE,
    REFILL_TRANSACTION_FACADE,
    PAYMENT_SAGA,
    WEB_CLIENT,
    TIPS_TRANSACTION_FACADE,
    TIPS_PRODUCT_SERVICE,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import (
    BaseModel,
    TokenWalletModel,
    TokenPackageModel,
    TokenRateModel,
    TransactionModel,
    ProductRefillModel,
    ProductTipsModel
)
from models.interfaces import InterfaceProductModel
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
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

# Main app instance creation
app = web.Application()

# Settings singleton initialization
settings = Settings()
app[SETTINGS] = settings

# DAO initialization
refill_product_dao = RefillProductDAO(app)
token_package_dao = TokenPackageDAO(app)
token_wallet_dao = TokenWalletDAO(app)
transaction_dao = TransactionDAO(app)
token_rate_dao = TokenRateDAO(app)
tips_product_dao = TipsProductDAO(app)

# Service initialization
app[WEB_CLIENT] = WebClient()
app[PAYMENT_SAGA] = PaymentSaga(web_client=app[WEB_CLIENT])
app[TRANSACTION_SERVICE] = TransactionService(transaction_dao=transaction_dao)
app[TOKEN_WALLET_SERVICE] = TokenWalletService(token_wallet_dao=token_wallet_dao)
app[TOKEN_PACKAGE_SERVICE] = TokenPackageService(token_package_dao=token_package_dao)
app[TOKEN_RATE_SERVICE] = TokenRateService(token_rate_dao=token_rate_dao)
app[REFILL_PRODUCT_SERVICE] = RefillProductService(refill_product_dao=refill_product_dao)
app[TIPS_PRODUCT_SERVICE] = TipsProductService(tips_product_dao=tips_product_dao)

# Facade initialization
app[REFILL_TRANSACTION_FACADE] = RefillTransactionFacade(
    app=app,
    refill_product_service=app[REFILL_PRODUCT_SERVICE],
    transaction_service=app[TRANSACTION_SERVICE],
    token_package_service=app[TOKEN_PACKAGE_SERVICE],
    token_rate_service=app[TOKEN_RATE_SERVICE],
    token_wallet_service=app[TOKEN_WALLET_SERVICE],
    payment_saga=app[PAYMENT_SAGA]
)
app[TIPS_TRANSACTION_FACADE] = TipsTransactionFacade(
    app=app,
    transaction_service=app[TRANSACTION_SERVICE],
    token_wallet_service=app[TOKEN_WALLET_SERVICE],
    tips_product_service=app[TIPS_PRODUCT_SERVICE]
)

# Middleware
app.middlewares.append(error_middleware)

# DB engine initialization
engine = create_async_engine(
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}/{settings.DB_NAME}",
    echo="debug",
)

# Sentry
sentry_sdk.init(
   dsn=settings.DSN,
   integrations=[AioHttpIntegration()]
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
app[DB_SESSION] = session


def get_app():
    return app