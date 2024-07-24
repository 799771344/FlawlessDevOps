from utils.mysql_utils import MysqlPool


class ImagesHouseModel(object):
    def __init__(self):
        self.table = "flawless_devops_images_house"
        self.mysql_pool = MysqlPool()

    async def insert_image_house(self, house_url, image_name, user_name, password):
        sql = f"insert into {self.table}(fd_house_url, fd_image_name, fd_username, fd_password) values (%s,%s,%s,%s)"
        args = [house_url, image_name, user_name, password]
        await self.mysql_pool.save_mysql(sql, args)