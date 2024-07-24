from utils.mysql_utils import MysqlPool


class FlowModel(object):
    def __init__(self):
        self.table = "flawless_devops_flow"
        self.mysql_pool = MysqlPool()

    def insert_flow(self):
        sql = f"insert into {self.table}(fd_)"