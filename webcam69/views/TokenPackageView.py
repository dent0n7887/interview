from dto import CreateTokenPackageDTO
from http import HTTPStatus
from aiohttp import web
from consts import TOKEN_PACKAGE_SERVICE


class RefillTransactionView(web.View):
    endpoint = "/api/token-package"

    async def post(self):

        data = await self.request.json()
        dto = CreateTokenPackageDTO(**data)
        package = await self.request.app[TOKEN_PACKAGE_SERVICE].create(dto)

        return web.json_response(status=HTTPStatus.OK, data=package.as_dict())

    async def get(self):

        packages = await self.request.app[TOKEN_PACKAGE_SERVICE].get_all()
        data = [package.as_dict() for package in packages]

        return web.json_response(status=HTTPStatus.OK, data=data)