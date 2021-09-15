from http import HTTPStatus
from aiohttp import web
from consts import REFILL_TRANSACTION_FACADE
from dto import TransactionRefillPaymentDTO


class RefillTransactionDetailView(web.View):
    endpoint = "/api/transaction/refill/{transaction_id}"

    async def patch(self):
        transaction_id = self.request.match_info.get('transaction_id')
        data = await self.request.json()
        data['transaction_id'] = transaction_id
        dto = TransactionRefillPaymentDTO(**data)

        transaction = await self.request.app[REFILL_TRANSACTION_FACADE].process_update(dto)

        return web.json_response(status=HTTPStatus.OK, data=transaction.as_dict())
