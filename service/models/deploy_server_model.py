from utils.mysql_utils import MysqlPool


class DeployServerModel(object):
    def __init__(self):
        self.table = "flawless_devops_deploy_server"
        self.mysql_pool = MysqlPool()