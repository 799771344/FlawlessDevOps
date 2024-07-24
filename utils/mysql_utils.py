import asyncio

import aiomysql
from common.mysql_db import mysql_config


class MysqlPool(object):
    def __init__(self, table_name="personal_blog", cursorclass="dict"):
        self.config = mysql_config.get_mysql_config(table_name)
        if cursorclass == "dict":
            self.cursorclass = aiomysql.DictCursor
        elif cursorclass == "tuple":
            self.cursorclass = aiomysql.Cursor
        # asyncio.ensure_future(self.create_mysql_pool())

    async def get_mysql_connection(self):
        loop = asyncio.get_event_loop()
        conn = await aiomysql.connect(
            host=self.config["host"],  # 指定数据库连接的主机地址
            port=self.config["port"],  # 指定数据库连接的端口号
            user=self.config["user"],  # 指定数据库连接的用户名
            password=self.config["password"],  # 指定数据库连接的密码
            db=self.config["database"],  # 指定要连接的数据库名称
            charset="utf8mb4",  # 指定字符集
            loop=loop,
            autocommit=True,
        )

        return conn

    async def save_mysql(self, sql, args=[], is_get_rowcount=False, conn=None):
        close_conn = False
        if conn is None:
            conn = await self.get_mysql_connection()
            close_conn = True

        try:
            async with conn.cursor(self.cursorclass) as cursor:
                new_id = None
                if len(args) > 0:
                    await asyncio.wait_for(cursor.execute(sql, args), timeout=60.0)
                else:
                    await asyncio.wait_for(cursor.execute(sql), timeout=60.0)
                rowcount = cursor.rowcount
                if rowcount > 0:
                    new_id = cursor.lastrowid

                if is_get_rowcount:
                    return rowcount
                return new_id
        finally:
            if close_conn:
                conn.close()

    async def select_mysql(self, sql, args=[]):
        conn = await self.get_mysql_connection()
        async with conn.cursor(self.cursorclass) as cursor:  # 指定游标类为aiomysql.DictCursor
            if len(args) > 0:
                await asyncio.wait_for(cursor.execute(sql, args), timeout=3600.0)  # 设置SQL执行超时为5秒
            else:
                await asyncio.wait_for(cursor.execute(sql), timeout=3600.0)  # 设置SQL执行超时为5秒
            result = await cursor.fetchone()
            conn.close()
            return result

    async def select_mysql_all(self, sql, args=[]):
        conn = await self.get_mysql_connection()
        async with conn.cursor(self.cursorclass) as cursor:  # 指定游标类为aiomysql.DictCursor
            if len(args) > 0:
                await asyncio.wait_for(cursor.execute(sql, args), timeout=3600.0)  # 设置SQL执行超时为5秒
            else:
                await asyncio.wait_for(cursor.execute(sql), timeout=3600.0)  # 设置SQL执行超时为5秒
            result = await cursor.fetchall()
            conn.close()
            return result

    async def select_mysql_all_yield(self, sql, args=[], batch_size=10):
        conn = await self.get_mysql_connection()
        async with conn.cursor(self.cursorclass) as cursor:  # 指定游标类为aiomysql.DictCursor
            if len(args) > 0:
                await asyncio.wait_for(cursor.execute(sql, args), timeout=3600.0)  # 设置SQL执行超时为5秒
            else:
                await asyncio.wait_for(cursor.execute(sql), timeout=3600.0)  # 设置SQL执行超时为5秒
            while True:
                result = await cursor.fetchmany(batch_size)
                if not result or len(result) < 1:
                    conn.close()
                    raise StopAsyncIteration
                yield result

    async def transaction(self):
        conn = await self.get_mysql_connection()
        try:
            await conn.begin()
            return conn
        except:
            await conn.close()
            raise