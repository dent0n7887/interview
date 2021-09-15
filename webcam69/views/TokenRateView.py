from dto import CreateTokenRateDTO
from http import HTTPStatus
from aiohttp import web
from consts import TOKEN_RATE_SERVICE


class RefillTransactionView(web.View):
    endpoint = "/api/token-rate"

    async def post(self):
        data = await self.request.json()
        dto = CreateTokenRateDTO(**data)
        package = await self.request.app[TOKEN_RATE_SERVICE].create(dto)

        return web.json_response(status=HTTPStatus.OK, data=package.as_dict())

    async def get(self):
        packages = await self.request.app[TOKEN_RATE_SERVICE].get_all()
        data = [package.as_dict() for package in packages]

        return web.json_response(status=HTTPStatus.OK, data=data)