import polaroid

from utils.decorators import with_executor
from .exceptions import ManipulationError

from PIL import Image as PillowImage
from PIL.Image import Image as PillowImageType
from PIL import ImageOps as PillowOps
from typing import Union, Tuple, Dict
from io import BytesIO



class PolaroidClient:
    def __init__(self) -> None:
        ...

    @with_executor
    def run_method(self, image: polaroid.Image, method: str, *args, **kwargs) -> polaroid.Image:
        method = getattr(image, method, None)
        if method is None:
            raise ManipulationError("Image Method is invalid")
        
        possible_result = method(*args, **kwargs)

        return image if possible_result is None else possible_result
    
    def create_image(self, image: bytes) -> polaroid.Image:
        return polaroid.Image(image)
    

            

class PillowClient:
    DISCORD_BG = "#36393f"
    CRIMSON = "#ff0000"
    IMAGETYPE = PillowImageType
    IMAGELIB = PillowImage

    def __init__(self) -> None:
        self.masks: Dict[str, PillowImageType] = {}
    
    def create_image(self, image: Union[str, BytesIO]) -> PillowImageType:
        if isinstance(image, str):
            img = PillowImage.open(image)
        else:
            img = PillowImage.open(BytesIO(image))
        return img
    

    @with_executor
    def run_image_method(self, image: PillowImageType, method: str, *args, **kwargs) -> PillowImageType:
        method = getattr(image, method, None)
        if method is None:
            raise ManipulationError("Image Method is invalid")
        
        possible_result = method(*args, **kwargs)
        return image if possible_result is None else possible_result

    @with_executor
    def create_empty_image(self, mode: str, size: Tuple[int, int], color: Union[int, str, Tuple[int, int, int]]) -> PillowImageType:
        img = PillowImage.new(mode, size, color)
        return img

    @with_executor
    def apply_mask(self, image: PillowImageType, mask__: str, centering: Tuple[float, float]) -> PillowImageType:
        mask = self.get_mask(mask__)
        fitted = PillowOps.fit(image, image.size, centering = centering)
        fitted.putalpha(mask)
        return fitted

    @with_executor
    def run_raw_image_method(self, method: str, *args, **kwargs):
        return getattr(PillowImage, method)(*args, **kwargs)

    def get_mask(self, mask: str) -> PillowImageType:
        mask_identifier = f"./assets/masks/{mask}"
        mask_cache = self.masks.get(mask_identifier)
        if mask_cache is not None:
            return mask_cache
        
        mask_make = PillowImage.open(mask_identifier).convert("L")
        self.masks[mask_identifier] = mask_make
        return mask_make

    @with_executor
    def get_mask_async(self, mask: str):
        return self.get_mask(mask)

    @with_executor
    def run_ops_method(self, method: str, *args, **kwargs):
        method = getattr(PillowOps, method, None)
        if method is None:
            raise ManipulationError("Invalid Ops Method")
        
        image = method(*args, **kwargs)
        return image

    

    def calculate_overlay(self, color, overlay):
        if color < 33:
            return overlay - 100
        elif color > 233:
            return overlay + 100
        else:
            return overlay - 133 + color


    @with_executor
    def apply_colour_overlay(self, image, color):
        overlay_red, overlay_green, overlay_blue = color
        channels = image.split()

        r = channels[0].point(lambda color: self.calculate_overlay(color, overlay_red))
        g = channels[1].point(lambda color: self.calculate_overlay(color, overlay_green))
        b = channels[2].point(lambda color: self.calculate_overlay(color, overlay_blue))


        channels[0].paste(r)
        channels[1].paste(g)
        channels[2].paste(b)

        return PillowImage.merge(image.mode, channels)