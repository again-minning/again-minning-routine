from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from base.database.connection import Connection
from base.database.utils import connect_to_mongo, close_mongo_connection
from base.exception.exception import MinningException, common_exception_response
from base.utils.constants import ConnectionMode
from retrospect import retrospect_routers
from routine import routine_routers, routine_batch_router
from report import report_batch_router, report_router

Connection(ddl_mode=ConnectionMode.NONE)
app = FastAPI()

app.include_router(routine_routers.router)
app.include_router(routine_batch_router.router)
app.include_router(retrospect_routers.router)
app.include_router(report_batch_router.router)
app.include_router(report_router.router)

app.add_event_handler('startup', connect_to_mongo)
app.add_event_handler('shutdown', close_mongo_connection)


@app.exception_handler(MinningException)
async def not_found_exception_handler(request: Request, exc: MinningException):
    return await common_exception_response(exc, request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await common_exception_response(exc, request)
