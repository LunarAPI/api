import uvicorn
import asyncio
import sys

from fastapi import FastAPI
from routes.images import polaroid_, pillow_
from routes.ml import chatbot
from routes.cv import cv2_
from routes.data import local


class App(FastAPI):
    loop = asyncio.get_event_loop()
    ROUTERS = [
        polaroid_.router,
        pillow_.router,
        cv2_.router,
        chatbot.router,
        local.router
    ]


app = App(debug = True)

for router in app.ROUTERS:
    app.include_router(router)

if ".\\launcher.py" in sys.argv:
    uvicorn.run(app, debug = True, port = 7000)