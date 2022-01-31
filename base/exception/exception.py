from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse


class MinningException(Exception):
    def __init__(self, name: str):
        self.name = name


async def common_exception_response(exc, request):
    content = await define_exception_content(exc, request)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            content
        )
    )


async def define_exception_content(exc, request):
    content = {
        'method': request.scope['method'],
        'type': request.scope['type'],
        'path': request.scope['path'],
        'path_params': request.scope['path_params'],
        'server': request.scope['server'],

    }
    if type(exc) is RequestValidationError:
        content.update({'detail': exc.errors(),
                        'body': exc.body})
    else:
        content.update({'body': exc.name})
    return content
