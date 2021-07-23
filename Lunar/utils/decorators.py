import asyncio
import functools


def with_executor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        partial = functools.partial(func, *args,  **kwargs)
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, partial)

    return wrapper