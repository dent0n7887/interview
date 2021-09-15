from dto import WalletCreateDTO
from http import HTTPStatus
from aiohttp import web
from consts import TOKEN_WALLET_SERVICE
from webargs.aiohttpparser import use_args
from webargs import fields
from utils.AppMiddleware import HandleError


class RefillTransactionView(web.View):
    endpoint = "/api/wallet"

    async def post(self):

        data = await self.request.json()
        dto = WalletCreateDTO(**data)
        wallet = await self.request.app[TOKEN_WALLET_SERVICE].create_wallet(dto)

        return web.json_response(status=HTTPStatus.OK, data=wallet.as_dict())

    @use_args({"user_id": fields.Str(required=False)}, location='query')
    async def get(self, args):
        user_id = args.get('user_id')

        if not user_id:
            raise HandleError('need user_id')

        wallets = await self.request.app[TOKEN_WALLET_SERVICE].get_by_user(user_id)
        data = [wallet.as_dict() for wallet in wallets]

        return web.json_response(status=HTTPStatus.OK, data=data)