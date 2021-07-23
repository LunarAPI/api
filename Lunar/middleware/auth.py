from fastapi import Request




async def authorize_request(request: Request, call_next):
    print(request.headers)

    route_response = await call_next(request)

    return route_response
    