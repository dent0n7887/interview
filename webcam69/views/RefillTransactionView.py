from dto import TransactionRefillRequestDTO
from http import HTTPStatus
from aiohttp import web
from consts import REFILL_TRANSACTION_FACADE


class RefillTransactionView(web.View):
    endpoint = "/api/transaction/refill"

    async def post(self):

        data = await self.request.json()
        dto = TransactionRefillRequestDTO(**data)
        transaction = await self.request.app[REFILL_TRANSACTION_FACADE].process_create(dto)

        return web.json_response(status=HTTPStatus.OK, data=transaction.as_dict())
