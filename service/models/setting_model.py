from utils.mysql_utils import MysqlPool


class SettingModel(object):

    def __init__(self):
        self.table = "flawless_devops_setting"
        self.mysql_pool = MysqlPool()

    async def get_token_key(self):
        sql = f"select fd_token_key from {self.table}"
        resutls = await self.mysql_pool.select_mysql(sql)
        token_key = resutls['fd_token_key']
        return token_key
