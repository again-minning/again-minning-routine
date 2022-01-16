from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from base.database.connection import CONNECTION
from retrospect import retrospectRouters
from routine import routine_routers
connection = CONNECTION
app = FastAPI()

app.include_router(routine_routers.router)
app.include_router(retrospectRouters.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                'method': request.scope['method'],
                'type': request.scope['type'],
                'path': request.scope['path'],
                'path_params': request.scope['path_params'],
                'server': request.scope['server'],
                'detail': exc.errors(),
                'body': exc.body
            }
        )
    )
