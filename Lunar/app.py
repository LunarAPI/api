import asyncio

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from routes.images import polaroid_, pillow_
from routes.ml import chatbot
from routes.cv import cv2_
from routes.data import local

from middleware.auth import authorize_request

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
app.add_middleware(BaseHTTPMiddleware, dispatch = authorize_request)
