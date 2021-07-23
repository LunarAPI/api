import cv2
import numpy

from fastapi import APIRouter
from Lunar import cv2_client, async_http

from fastapi.responses import Response
from typing import Optional

router = APIRouter()

@router.get("/cv/edge-detect")
async def edge_detect(url: str):
    image = await async_http.read_url(url)
    array = await cv2_client.read_image(image)
    img_gray = await cv2_client.run_lib_method("cvtColor", array, cv2.COLOR_BGR2GRAY)
    img_blur = await cv2_client.run_lib_method("GaussianBlur", img_gray, (3,3), 0)
    edges = await cv2_client.run_lib_method("Sobel", src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    buffer = await cv2_client.save_image(edges)
    return Response(buffer.getvalue(), media_type = "image/jpg")

@router.get("/cv/face-detect")
async def face_detect(url: str, mn: Optional[float] = 1.3, sf: Optional[int] = 4):
    image = await async_http.read_url(url)
    array = await cv2_client.read_image(image)
    img_gray = await cv2_client.run_lib_method("cvtColor", array, cv2.COLOR_BGR2GRAY)
    faces = await cv2_client.run_client_property_method(cv2_client.face_cascade, "detectMultiScale", img_gray, mn, sf)
    for (x, y, w, h) in faces:
        await cv2_client.run_lib_method("rectangle", array, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    buffer = await cv2_client.save_image(array)
    return Response(buffer.getvalue(), media_type="image/jpg")

@router.get("/cv/colour-detect")
async def colour_detect(url: str, r: int, g: int, b: int):
    colour = numpy.array([r, g, b])
    black = numpy.array([255,255,255])
    image = await async_http.read_url(url)
    array = await cv2_client.read_image(image)
    hsv = await cv2_client.run_lib_method("cvtColor", array, cv2.COLOR_BGR2HSV)
    mask = await cv2_client.run_lib_method("inRange", hsv, colour, black)
    output = await cv2_client.run_lib_method("bitwise_and", array, array, mask = mask)
    buffer = await cv2_client.save_image(output)
    return Response(buffer.getvalue(), media_type = "image/jpg")