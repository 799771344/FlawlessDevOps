import uuid

from utils.common_utils import CommonUtils
from common.exception import CustomHTTPException, CustomException, mysql_error
from utils.mysql_utils import MysqlPool
from utils.token_utils import TokenUtils
from service.models.user_model import UserModel


class Register(object):

    def __init__(self, username, password, email):
        fixed_key = "21_5OwUtU0Rzsof2zA9F3k5LgZgxnfjXKD_lPC30tbQ="  # 密钥
        self.username = username
        self.password = password
        self.email = email
        self.mysql_pool = MysqlPool()
        self.common_utils = CommonUtils(fixed_key)
        self.user_model = UserModel()

    async def create(self):
        if not await self.common_utils.is_valid_email(self.email):
            raise CustomHTTPException(msg="邮箱格式有误")
        password = await self.common_utils.hash_password(self.password)
        session_id = str(uuid.uuid4())
        user_id = await self.user_model.insert_user(self.username, password, self.email, session_id)
        return user_id


class Login(object):

    def __init__(self):
        self.mysql_pool = MysqlPool()
        self.token_utils = TokenUtils()
        self.common_utils = CommonUtils()
        self.user_model = User()

    async def get_user_token(self, email, password):
        password = await self.common_utils.hash_password(password)
        user_info = await self.user_model.get_user_info_by_email(email, password)
        if user_info is None:
            raise CustomHTTPException(msg="登录失败，用户不存在或账号密码错误")
        token = await self.token_utils.generate(user_info['pb_id'], user_info['pb_session_id'])
        return token, user_info['pb_id']

    async def get_user_info(self, token):
        payload = await self.token_utils.parse(token)
        user_id = payload['user_id']
        user_session_id = payload['user_session_id']
        select_sql = "select pb_id, pb_username, pb_email from personal_blog_user where pb_id = %s and pb_session_id = %s"
        user_info = await self.mysql_pool.select_mysql(select_sql, [user_id, user_session_id])
        return user_info
