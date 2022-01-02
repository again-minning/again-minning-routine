from fastapi import FastAPI
from routine import routineRouters
from retrospect import retrospectRouters
from base.database.connection import CONNECTION

connection = CONNECTION
app = FastAPI()

app.include_router(routineRouters.router)
app.include_router(retrospectRouters.router)
