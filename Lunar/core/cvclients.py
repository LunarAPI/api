import cv2
import numpy

from utils.decorators import with_executor
from core.exceptions import ManipulationError

from io import BytesIO
from typing import Union, Any


class OpenCVClient:
    def __init__(self) -> None:
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    @with_executor
    def read_image(self, image: Union[bytes, BytesIO]) -> numpy.ndarray:
        image = image if not isinstance(image, BytesIO) else image.getvalue()
        array = numpy.frombuffer(image, dtype = numpy.uint8)
        img = cv2.imdecode(array, cv2.IMREAD_COLOR)
        return img

    @with_executor
    def run_lib_method(self, method: str, *args, **kwargs) -> numpy.ndarray:
        method = getattr(cv2, method, None)
        if method is None:
            raise ManipulationError("Invalid cv2 method")
        
        result = method(*args, **kwargs)
        return result


    @with_executor
    def save_image(self, image: numpy.ndarray) -> BytesIO:
        _, bytes__ = cv2.imencode(".jpg", image)
        buffer = BytesIO(bytes__)
        return buffer

    @with_executor
    def run_client_property_method(self, property__: Any, method: str, *args, **kwargs):
        method = getattr(property__, method, None)
        if method is None:
            raise ManipulationError("Invalid cv2 method")
        
        result = method(*args, **kwargs)
        return result
