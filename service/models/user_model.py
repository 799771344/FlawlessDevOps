from utils.mysql_utils import MysqlPool


class UserModel(object):

    def __init__(self):
        self.mysql_pool = MysqlPool()
        self.table = "flawless_devops_user"

    async def get_user_info_by_id(self, user_id):
        sql = f"SELECT * FROM {self.table} WHERE fd_id = %s"
        args = [user_id]
        results = await self.mysql_pool.select_mysql(sql, args)
        return results

    async def insert_user(self, username, password, email, session):
        sql = f"INSERT INTO {self.table} (fd_username, fd_email, fd_password, fd_session) VALUES (%s, %s, %s, %s)"
        args = [username, email, password, session]
        user_id = await self.mysql_pool.save_mysql(sql, args)
        return user_id

    async def get_user_info_by_email(self, email, password):
        sql = f"SELECT * FROM {self.table} WHERE fd_email = %s AND fd_password = %s"
        args = [email, password]
        results = await self.mysql_pool.select_mysql(sql, args)
        return results

    async def verify_user(self, user_id, session):
        sql = f"select count(1) from {self.table} where fd_id=%s and fd_session=%s"
        args = [user_id, session]
        results = await self.mysql_pool.select_mysql(sql, args)
        return results

