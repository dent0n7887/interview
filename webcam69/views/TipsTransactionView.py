from dto import TransactionTipsRequestDTO
from http import HTTPStatus
from aiohttp import web
from consts import TIPS_TRANSACTION_FACADE


class RefillTransactionView(web.View):
    endpoint = "/api/transaction/tips"

    async def post(self):

        data = await self.request.json()
        dto = TransactionTipsRequestDTO(**data)
        transaction = await self.request.app[TIPS_TRANSACTION_FACADE].process(dto)

        return web.json_response(status=HTTPStatus.OK, data=transaction.as_dict())
