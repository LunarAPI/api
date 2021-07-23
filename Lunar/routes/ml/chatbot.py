from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from Lunar import chatbot
router = APIRouter()


@router.websocket("/ml/chatbot-ws")
async def chatbot_ws(ws: WebSocket):
    # TODO: allow for OP Code events and JSON communication.
    await ws.accept()
    try:
        while True:
            text = await ws.receive_text()
            response = await chatbot.get_response(text)
            await ws.send_text(response)
    except WebSocketDisconnect as exc:
        pass



        

@router.get("/ml/chatbot")
async def chatbot_normal(text: str):
    response = await chatbot.get_response(text)
    data = {
        "input": text,
        "output": response
    }
    return JSONResponse(data)


