import aiohttp

from .exceptions import CouldNotReadImage

class AsyncHTTPClient:
    def __init__(self) -> None:
        self.session = None

    async def validate_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        
    

    async def read_url(self, url: str) -> bytes:
        await self.validate_session()

        try:
            async with self.session.get(url) as resp:
                img = await resp.read()
        except Exception as exc:
            raise CouldNotReadImage(exc)

        return img

        