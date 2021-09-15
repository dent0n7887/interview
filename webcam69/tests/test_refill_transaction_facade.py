from mockito import when, unstub
from tests import conftest


class TestRefillTransactionFacade:

    def teardown(self):
        unstub()

    def test_refill_transaction_facade_pending(
            self,
            loop,
            f_transaction_refill_request_dto,
            f_token_package_model,
            f_token_rate_model,
            f_product_refill_model,
            f_transaction_model_pending,
            f_transaction_refill_payment_dto_pending,
            f_refill_order_facade,
    ):
        async def do_test():

            async def f_token_package_result():
                return f_token_package_model

            async def f_token_rate_result():
                return f_token_rate_model

            async def f_product_refill_result():
                return f_product_refill_model

            async def f_transaction_refill_pending_result():
                return f_transaction_model_pending

            async def f_payment_refill_pending_result():
                return f_transaction_refill_payment_dto_pending

            when(conftest.TokenPackageDAO).get_by_id(...).thenReturn(f_token_package_result())
            when(conftest.TokenRateDAO).get_by_currency(...).thenReturn(f_token_rate_result())
            when(conftest.RefillProductDAO).create(...).thenReturn(f_product_refill_result())
            when(conftest.TransactionDAO).create(...).thenReturn(f_transaction_refill_pending_result())
            when(conftest.PaymentSaga).create_payment(...).thenReturn(f_payment_refill_pending_result())
            when(conftest.TransactionDAO).update(...).thenReturn(f_transaction_refill_pending_result())
            when(conftest.RefillProductDAO).update(...).thenReturn(f_product_refill_result())
            when(conftest.TransactionDAO).get_by_id(...).thenReturn(f_transaction_refill_pending_result())

            transaction = await f_refill_order_facade.process_create(
                transaction_refill_request=f_transaction_refill_request_dto
            )

            assert transaction == f_transaction_model_pending

        loop.run_until_complete(do_test())

    def test_refill_transaction_facade_completed(
            self,
            loop,
            f_transaction_refill_request_dto,
            f_token_package_model,
            f_token_rate_model,
            f_product_refill_model,
            f_transaction_model_complete,
            f_transaction_refill_payment_dto_completed,
            f_refill_order_facade,
    ):
        async def do_test():
            async def f_token_package_result():
                return f_token_package_model

            async def f_token_rate_result():
                return f_token_rate_model

            async def f_product_refill_result():
                return f_product_refill_model

            async def f_transaction_refill_complete_result():
                return f_transaction_model_complete

            async def f_payment_refill_complete_result():
                return f_transaction_refill_payment_dto_completed

            when(conftest.TokenPackageDAO).get_by_id(...).thenReturn(f_token_package_result())
            when(conftest.TokenRateDAO).get_by_currency(...).thenReturn(f_token_rate_result())
            when(conftest.RefillProductDAO).create(...).thenReturn(f_product_refill_result())
            when(conftest.TransactionDAO).create(...).thenReturn(f_transaction_refill_complete_result())
            when(conftest.PaymentSaga).create_payment(...).thenReturn(f_payment_refill_complete_result())
            when(conftest.TransactionDAO).update(...).thenReturn(f_transaction_refill_complete_result())
            when(conftest.RefillProductDAO).update(...).thenReturn(f_product_refill_result())
            when(conftest.TransactionDAO).get_by_id(...).thenReturn(f_transaction_refill_complete_result())
            when(conftest.TokenWalletDAO).change_balance(...).thenReturn(f_product_refill_result())

            transaction = await f_refill_order_facade.process_create(
                transaction_refill_request=f_transaction_refill_request_dto
            )

            assert transaction == f_transaction_model_complete

        loop.run_until_complete(do_test())
