import os
import sys


# 获取当前文件路径
current_path = os.path.abspath(__file__)
# 获取上级目录
parent_path = os.path.dirname(current_path)
# 获取上上级目录
file_path = os.path.dirname(parent_path)
sys.path.append(file_path)

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from common.exception import CustomHTTPException, CustomExpiredSignatureError
from fastapi import Request
from utils.token_utils import TokenUtils


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_url = str(request.url)
        ex_url = ("/login", '/register')
        is_ok_num = 0
        for u in ex_url:
            if u in request_url:
                is_ok_num += 1
        if is_ok_num == 0:
            authorization: str = request.headers.get("Authorization")
            if authorization is None or not authorization.startswith('Bearer '):
                return await CustomHTTPException(msg="Unauthorized").to_response()
            try:
                verify_res = await TokenUtils().verify(authorization.replace("Bearer ", ""))
            except CustomExpiredSignatureError as e:
                return await e.to_response()
            if not verify_res:
                return await CustomHTTPException(code=401, msg="Unauthorized").to_response()
        response = await call_next(request)
        return response
