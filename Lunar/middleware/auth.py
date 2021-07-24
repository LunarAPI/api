from fastapi import Request




async def authorize_request(request: Request, call_next):
    print(request.headers)
    print(request.state)
    print(request.cookies)

    route_response = await call_next(request)

    return route_response
    