import aiohttp

from core.imageclients import PolaroidClient, PillowClient
from core.httpclients import AsyncHTTPClient
from core.mlclients import ChatBot
from core.cvclients import OpenCVClient

LOAD_CHATBOT = False



polaroid_client = PolaroidClient()
pillow_client = PillowClient()
async_http = AsyncHTTPClient()
cv2_client = OpenCVClient()

chatbot = ChatBot(LOAD_CHATBOT)
