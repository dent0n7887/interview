import json
from http import HTTPStatus
import pydantic
from aiohttp import web


@web.middleware
async def error_middleware(request: web.Request, handler) -> web.Response:
    try:
        return await handler(request)
    except pydantic.ValidationError as err:
        return web.json_response(
            {"Wrong value(s):": err.errors()}, status=HTTPStatus.BAD_REQUEST
        )
    except json.JSONDecodeError:
        return web.json_response(
            {"error": "json decode error"}, status=HTTPStatus.BAD_REQUEST
        )
    except HandleError as err:
        return web.json_response(err.data, status=HTTPStatus.BAD_REQUEST)
    except HandleDBError as err:
        return web.json_response(err.data, status=HTTPStatus.BAD_REQUEST)


class HandleError(Exception):

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


class HandleDBError(Exception):

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)