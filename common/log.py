import logging
import logging.handlers
import asyncio
from common.file_path import file_path

class AsyncLoggingConfig:

    def __init__(self,
                 log_file_name="FlawlessDevOps",
                 log_level=logging.DEBUG,
                 max_bytes=1000 * 1024 * 1024,
                 backup_count=10,
                 log_name=None):
        self.log_file = "{}/log/{}.log".format(file_path, log_file_name)
        self.log_level = log_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.log_name = log_name
        self.logger = None  # 添加一个属性来存储 logger

    async def get_logger(self, log_name=None):
        if self.logger:  # 如果 logger 已经存在，则直接返回
            return self.logger

        _log_name = []
        _log_name.append(self.log_name) if self.log_name else None
        _log_name.append(log_name) if log_name else None
        _log_name = ".".join(_log_name) if _log_name else None

        logging.basicConfig()
        self.logger = logging.getLogger(_log_name)

        # 清除所有 handler
        self.logger.handlers.clear()

        # 添加新的 handler
        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)-8s - %(filename)s:%(lineno)s - {} : %(message)s '.format(_log_name))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(self.log_level)
        return self.logger

# 示例用法
async def main():
    logging_config = AsyncLoggingConfig(log_file_name="TestLog")
    logger = await logging_config.get_logger("TestLogger")
    logger.info("This is a test log message.")

if __name__ == "__main__":
    asyncio.run(main())