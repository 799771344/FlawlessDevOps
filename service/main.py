import os
import sys


# 获取当前文件路径
current_path = os.path.abspath(__file__)
# 获取上级目录
parent_path = os.path.dirname(current_path)
# 获取上上级目录
file_path = os.path.dirname(parent_path)
sys.path.append(file_path)

import uvicorn

from service.middlewares.auth_middleware import AuthMiddleware
from service.urls import urls
from fastapi import FastAPI
from fastapi.routing import APIRouter
from common.init_yaml import yaml_data
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()
app.add_middleware(AuthMiddleware)
# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头
)


def add_route():
    if len(urls) > 0:
        for _url in urls:
            route_path = _url[0]
            handler = _url[1]
            if len(_url) > 2:
                methods = _url[2]
            else:
                methods = ["GET", "POST"]
            router.add_api_route(route_path, handler, methods=methods)
            app.include_router(router)


# async def add_route(methods, url_path, func_handle):
#     router.add_api_route(url_path, func_handle, methods=methods)
#     app.include_router(router)


if __name__ == '__main__':
    add_route()
    host = yaml_data["service"]['service']["host"]
    port = yaml_data["service"]['service']["port"]
    uvicorn.run(app, host=host, port=port)
