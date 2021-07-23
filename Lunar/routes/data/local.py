import aiofiles
import random

from fastapi import APIRouter

from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/data/joke")
async def get_joke():
    # https://pastebin.com/YqrYRC3K
    async with aiofiles.open("./assets/data/jokes.txt") as f:
        contents = await f.read()
    
    joke = random.choice(contents.split(","))
    joke = joke.replace("\n", "")
    data = {
        "joke": joke
    }

    return JSONResponse(data)

    

@router.get("/data/fact")
async def get_fact():
    # https://pastebin.com/cqpQfLiH
    async with aiofiles.open("./assets/data/facts.txt") as f:
        contents = await f.read()
    
    fact = random.choice(contents.split(";"))
    fact = fact.replace("\n", "")
    data = {
        "fact": fact
    }

    return JSONResponse(data)

    
    
        
    