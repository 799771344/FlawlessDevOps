from service.controllers.add_flow import AddFlow
from service.controllers.flow_setting import FlowSetting
from service.controllers.flow_list import FlowList
from service.controllers.flow_detail import FlowDetail
from service.controllers.user import Register,Login
from utils.common_utils import log_request_response
from common.exception import CustomHTTPException


@log_request_response
async def get_flow_list(request, **kwargs):
    ind = FlowList()
    res = await ind.get_all_article()
    return res


@log_request_response
async def login(request, **kwargs):
    email = request.get('email')
    password = request.get('password')
    if email is None or password is None:
        raise CustomHTTPException(msg="请输入账号和密码")
    logi = Login()
    token, user_id = await logi.get_user_token(request['email'], request['password'])
    return {"token": token, "user_id": user_id}


@log_request_response
async def get_flow_detail(request, **kwargs):
    token = kwargs['headers'].get("authorization")
    token = token.replace("Bearer ", "")
    logi = FlowDetail()
    user_info = await logi.get_user_info(token)
    return user_info


@log_request_response
async def register(request, **kwargs):
    email = request.get('email')
    username = request.get('username')
    password = request.get('password')
    regi = Register(username, password, email)
    user_id = await regi.create()
    return {"user_id": user_id}


@log_request_response
async def flow_setting(request, **kwargs):
    user_id = request.get('user_id')
    art = FlowSetting()
    res = await art.get_article_list(user_id)
    return res


@log_request_response
async def add_flow(request, **kwargs):
    token = kwargs['headers'].get("authorization")
    token = token.replace("Bearer ", "")
    article_id = request.get('article_id')
    art = AddFlow()
    res = await art.get_article_detail(article_id, token)
    return res
