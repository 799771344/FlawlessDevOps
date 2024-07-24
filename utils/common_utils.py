import gzip
import hashlib
import json
import os
import re
import socket
import time

from cryptography.fernet import Fernet
from fastapi import Request
from common.exception import CustomHTTPException, CustomException, CustomResponse, CustomExpiredSignatureError


def log_request_response(func):
    async def wrapper(request: Request):
        # 获取请求信息
        request_time = time.time()
        try:
            if request.method == "GET":
                request_data = dict(request.query_params)
            else:
                request_data = await request.json()
            print(f"Request data: {request_data}")

            # 执行被装饰的函数
            data = await func(request_data, headers=request.headers)

            # 获取响应信息
            response_time = time.time()
            response_duration = response_time - request_time
            print(f"Response duration: {response_duration:.2f} seconds")

            # 返回JSON响应
            return await CustomResponse(data=data).to_response()
        except CustomHTTPException as e:
            # 处理HTTPException
            return await e.to_response()
        except CustomExpiredSignatureError as e:
            return await e.to_response()
        except CustomException as e:
            # 处理其他异常
            return await e.to_response()
    return wrapper


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class CommonUtils(object):

    def __init__(self, fixed_key=None):
        if fixed_key:
            self.cipher_suite = Fernet(fixed_key)

    # 压缩
    async def compress(self, data):
        compressed_data = gzip.compress(json.dumps(data).encode('utf-8'))
        return compressed_data

    # 解压缩
    async def decompress(self, compressed_data):
        data = json.loads(gzip.decompress(compressed_data).decode('utf-8'))
        return data

    # 加密
    async def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data)
        return encrypted_data

    # 解密
    async def decrypt(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return decrypted_data

    async def hash_password_with_salt(self, password):
        salt = os.urandom(16)
        salted_password = salt + password.encode()
        hash_value = hashlib.sha256(salted_password).hexdigest()
        return salt, hash_value

    async def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    async def is_valid_email(self, email):
        # 定义邮箱格式的正则表达式
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # 使用 re.match() 方法匹配邮箱
        if re.match(email_regex, email):
            return True
        else:
            return False
