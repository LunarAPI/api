import asyncio

from Lunar import pillow_client, async_http
from PIL import Image, ImageSequence
from fastapi import APIRouter, Response
from io import BytesIO
from typing import Optional, Tuple

from utils import palletes, image
from core.exceptions import BadRequest


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


@router.get("/image/lego")
async def lego_image(url: str):
    image = await async_http.read_url(url)
    image = pillow_client.create_image(image)
    lego_brick = pillow_client.create_image("./assets/images/brick.ico")
    
    # reduce image
    legos = palletes.legos()
    new_size = image.size
    scale_x, scale_y = lego_brick.size

    if new_size[0] > scale_x or new_size[1] > scale_y:
        if new_size[0] < new_size[1]:
            scale = new_size[1] / scale_y
        else:
            scale = new_size[0] / scale_x

        new_size = (int(round(new_size[0] / scale)) or 1,
                    int(round(new_size[1] / scale)) or 1)

    gif = False
    if image.format == "GIF":
        gif = True

    if gif is False:
        base_image = image.resize(new_size, pillow_client.IMAGELIB.ANTIALIAS)
        base_width, base_height = base_image.size
        brick_width, brick_height = lego_brick.size
        lego_image = await pillow_client.run_raw_image_method("new", "RGB", (base_width * brick_width,
                                    base_height * brick_height), "white")
        rgb_image = await pillow_client.run_image_method(base_image, "convert", "RGB")
        for brick_x in range(base_width):
            for brick_y in range(base_height):
                color = rgb_image.getpixel((brick_x, brick_y))
                lego_image.paste(await pillow_client.apply_colour_overlay(lego_brick, color),
                                (brick_x * brick_width, brick_y * brick_height))

    else:
        converted_frames = []
        frame_iterator = ImageSequence.Iterator(image)
        if len([frame.copy() for frame in frame_iterator]) > 20:
            raise BadRequest("Amount of GIF Frames surpassed GIF Image Frame Limit")
        for frame in ImageSequence.Iterator(image):
            new_size = frame.size
            scale_x, scale_y = lego_brick.size

            if new_size[0] > scale_x or new_size[1] > scale_y:
                if new_size[0] < new_size[1]:
                    scale = new_size[1] / scale_y
                else:
                    scale = new_size[0] / scale_x

                new_size = (int(round(new_size[0] / scale)) or 1,
                            int(round(new_size[1] / scale)) or 1)

            base_image = await pillow_client.run_image_method(frame, "resize", new_size, pillow_client.IMAGELIB.ANTIALIAS)
            base_width, base_height = base_image.size
            brick_width, brick_height = lego_brick.size
            lego_image = await pillow_client.run_raw_image_method("new", "RGB", (base_width * brick_width,
                                        base_height * brick_height), "white")
            rgb_image = await pillow_client.run_image_method(base_image, "convert", "RGB")
            for brick_x in range(base_width):
                for brick_y in range(base_height):
                    color = rgb_image.getpixel((brick_x, brick_y))
                    lego_image.paste(await pillow_client.apply_colour_overlay(lego_brick, color),
                                    (brick_x * brick_width, brick_y * brick_height))

            converted_frames.append(lego_image)


        
        

    buffer = BytesIO()
    image_format = image.format.lower() or "png"
    lego_image.save(buffer, format = image_format) if image.format != "GIF" else converted_frames[0].save(buffer, loop = 0, format = image.format, save_all=True, append_images=converted_frames[1:])
    return Response(buffer.getvalue(), media_type = "image/{}".format(image_format))