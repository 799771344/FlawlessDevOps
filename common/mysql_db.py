from common.init_yaml import yaml_data


class MysqlConfig:
    def __init__(self):
        self.mysql_path = yaml_data["client"]["mysql"]

    def get_mysql_config(self, mysql_name):
        return {
            "host": self.mysql_path[mysql_name]["host"],
            "port": self.mysql_path[mysql_name]["port"],
            "user": self.mysql_path[mysql_name]["user"],
            "password": self.mysql_path[mysql_name]["password"],
            "database": self.mysql_path[mysql_name]["database"]
        }


mysql_config = MysqlConfig()
