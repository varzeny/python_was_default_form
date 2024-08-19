# middleware/access.py

# lib
from typing import Callable, Awaitable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from datetime import datetime, timezone

# l2
# from app.l2.content.account import 
import app.l2.authorization as AUTH

# definition
class AccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # 요청 전
        decoded_data = AUTH.get_token_from_cookie(req, "access_token")
        if decoded_data:
            req.state.access_token = AUTH.AccessToken(**decoded_data)
        else:
            req.state.access_token = AUTH.AccessToken()

        print("="*200)
        print(f"current time : {datetime.now(timezone.utc)}")
        print(f"access_token : { req.state.access_token.__dict__ }")
        print(f"token remain : {datetime.fromtimestamp(req.state.access_token.exp, timezone.utc)-datetime.now(timezone.utc)}")

        # 대기 중
        resp:Response = await call_next(req)

        # 요청 후
        access_token:AUTH.AccessToken = req.state.access_token
        access_token.extend_token()

        return AUTH.put_token_to_cookie(resp, access_token)
