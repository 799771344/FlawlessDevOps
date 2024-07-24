from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pymysql import IntegrityError, DataError, DatabaseError


class CustomHTTPException(HTTPException):
    def __init__(self, code: int = 400, msg: str = "", data: any = None):
        super().__init__(status_code=code, detail=msg, headers=data)
        self.code = code
        self.msg = msg
        self.data = data

    async def to_response(self):
        return JSONResponse({"code": self.code, "msg": self.msg, "data": self.data})


class CustomExpiredSignatureError(HTTPException):
    def __init__(self, code: int = 401, msg: str = "", data: any = None):
        super().__init__(status_code=code, detail=msg, headers=data)
        self.code = code
        self.msg = msg
        self.data = data

    async def to_response(self):
        return JSONResponse({"code": self.code, "msg": self.msg, "data": self.data})


class CustomException(Exception):
    def __init__(self, code: int = 500, msg: str = "", data: any = None):
        self.code = code
        self.msg = msg
        self.data = data

    async def to_response(self):
        return JSONResponse({"code": self.code, "msg": self.msg, "data": self.data})


class CustomResponse(object):

    def __init__(self, code: int = 200, msg: str = 'success', data: any = None):
        self.code = code
        self.msg = msg
        self.data = data

    async def to_response(self):
        return JSONResponse({"code": self.code, "msg": self.msg, "data": self.data})


def mysql_error(e):
    error_code, error_message = e.args
    if isinstance(e, IntegrityError):
        if error_code == 1062:
            if "unique_pb_username" in error_message:
                raise CustomHTTPException(msg="用户名已存在")
            elif "unique_pb_email" in error_message:
                raise CustomHTTPException(msg="邮箱已被注册")
            else:
                raise CustomHTTPException(msg="数据库中存在重复记录")
        elif error_code == 1452:
            raise CustomHTTPException(msg="外键约束违反")
        else:
            raise CustomHTTPException(msg=str(e))
    elif isinstance(e, DataError):
        if error_code == 1406:
            raise CustomHTTPException(msg="字段数据长度超过限制")
        else:
            raise CustomHTTPException(msg=str(e))
    elif isinstance(e, DatabaseError):
        if error_code in [1054, 1146]:
            raise CustomHTTPException(msg="数据库操作错误")
        else:
            raise CustomHTTPException(msg=str(e))
