import polaroid
from Lunar import polaroid_client, async_http
from fastapi import APIRouter
from fastapi.responses import Response
from polaroid import Rgb

from typing import Optional

router = APIRouter()


@router.get("/image/solarize")
async def solarize_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "solarize")
    return Response(img.save_bytes(), media_type="image/png")
    
@router.get("/image/invert")
async def invert_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "invert")
    return Response(img.save_bytes(), media_type="image/png")


@router.get("/image/blur")
async def blur_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "box_blur")
    return Response(img.save_bytes(), media_type=f"image/png")


@router.get("/image/emboss")
async def emboss_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "emboss")
    return Response(img.save_bytes(), media_type=f"image/png")

@router.get("/image/oil")
async def oil_image(url: str, radius: Optional[int] = 4, intensity: Optional[float] = 55.0):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "oil", radius, intensity)
    return Response(img.save_bytes(), media_type=f"image/png")


@router.get("/image/primary")
async def primary_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "primary")
    return Response(img.save_bytes(), media_type=f"image/png")

@router.get("/image/frostedglass")
async def frosted_glass_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "frosted_glass")
    return Response(img.save_bytes(), media_type=f"image/png")

@router.get("/image/halftone")
async def halftone_image(url: str):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "halftone")
    return Response(img.save_bytes(), media_type=f"image/png")

@router.get("/image/gradient")
async def gradient_image(url: str, r: int, g: int, b: int):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "gradient", Rgb(r, 0, 0), Rgb(0, g, 0), Rgb(0, 0, b))
    return Response(img.save_bytes(), media_type=f"image/png")



@router.get("/image/filter")
async def filter_image(url: str, filter: Optional[str] = "oceanic"):
    img = await async_http.read_url(url)
    img = polaroid_client.create_image(img)
    img = await polaroid_client.run_method(img, "filter", filter)
    return Response(img.save_bytes(), media_type=f"image/png")

