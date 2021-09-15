from typing import Any, Optional
from aiohttp import ClientResponse, ClientSession, ContentTypeError
from aiohttp.helpers import sentinel
from aiohttp.typedefs import LooseHeaders
from .dto import WebClientResponse


class WebClient:
    def __init__(self):
        self._session = ClientSession(raise_for_status=True)

    async def _get_json(
        self,
        response: ClientResponse,
    ):
        try:
            resp_json = await response.json()
        except ContentTypeError:
            resp_json = None

        return resp_json

    async def _create_client_response(self, response: ClientResponse):
        headers = response.headers
        status = response.status

        resp_json = await self._get_json(response=response)

        return WebClientResponse(
            body=resp_json,
            headers=headers,
            status=status,
        )

    async def close(self):
        await self._session.close()

    async def post(
        self,
        url: str,
        json: Any = None,
        headers: Optional[LooseHeaders] = None,
        timeout: int = sentinel,
    ) -> WebClientResponse:
        """
        :raises:
            aiohttp.ClientError
        """
        async with self._session.post(
            url=url,
            json=json,
            timeout=timeout,
            headers=headers,
        ) as response:
            response = await self._create_client_response(response=response)
        return response

    async def get(
            self,
            url: str,
            headers: Optional[LooseHeaders] = None,
            timeout: int = sentinel,
    ) -> WebClientResponse:
        async with self._session.get(
            url=url,
            headers=headers,
            timeout=timeout
        ) as response:
            response = await self._create_client_response(response=response)
            return response
