import asyncio

import jwt
import datetime

from jwt import ExpiredSignatureError

from common.exception import CustomExpiredSignatureError
from utils.mysql_utils import MysqlPool
from service.models.user_model import UserModel
from service.models.setting_model import SettingModel


class TokenUtils(object):

    def __init__(self):
        self.secret_key = None
        self.mysql_pool = MysqlPool()
        self.user_model = UserModel()
        self.setting_model = SettingModel()
        asyncio.ensure_future(self._get_token_key())

    async def _get_token_key(self):
        self.secret_key = await self.setting_model.get_token_key()

    async def generate(self, user_id, user_session):
        # 定义密钥和数据
        payload = {
            'user_id': user_id,
            'user_session': user_session,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 设置过期时间
        }

        # 生成JWT
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    async def parse(self, token):
        try:
            # 解码JWT
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except ExpiredSignatureError as e:
            raise CustomExpiredSignatureError(msg="Signature Expired")
        return decoded_payload

    async def verify(self, token):
        payload = await self.parse(token)
        user_id = payload['user_id']
        user_session = payload['user_session']
        exp = payload['exp']
        res = await self.user_model.verify_user(user_id, user_session)
        if res is None:
            return False
        return True
