import uvicorn
import asyncio
import sys

from fastapi import FastAPI
from Lunar.app import app


for router in app.ROUTERS:
    app.include_router(router)

if ".\\launcher.py" in sys.argv:
    uvicorn.run(app, debug = True, port = 7000)