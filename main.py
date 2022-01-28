from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from base.database.connection import Connection
from base.exception.exception import NotFoundException, common_exception_response
from base.utils.constants import ConnectionMode
from retrospect import retrospectRouters
from routine import routine_routers

Connection(ddl_mode=ConnectionMode.CREATE)
app = FastAPI()

app.include_router(routine_routers.router)
app.include_router(retrospectRouters.router)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return await common_exception_response(exc, request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await common_exception_response(exc, request)




