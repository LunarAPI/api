from Lunar import pillow_client, async_http
from fastapi import APIRouter, Response
from io import BytesIO
from typing import Optional

router = APIRouter()

@router.get("/image/flip")
async def flip_image(url: str):
    image = await async_http.read_url(url)
    image = pillow_client.create_image(image)
    image = await pillow_client.run_ops_method("flip", image)
    buffer = BytesIO()
    image_format = image.format or "png"
    image.save(buffer, format = image_format)
    return Response(buffer.getvalue(), media_type=f"image/{image_format}")


@router.get("/image/mirror")
async def mirror_image(url: str):
    image = await async_http.read_url(url)
    image = pillow_client.create_image(image)
    image = await pillow_client.run_ops_method("mirror", image)
    buffer = BytesIO()
    image_format = image.format or "png"
    image.save(buffer, format = image_format)
    return Response(buffer.getvalue(), media_type=f"image/{image_format}")

