from typing import Any
from time import sleep
from colorful_logger.logger import get_logger
from HioT.Plugins.get_config import global_config

logger = get_logger(name="main",
                    level=global_config['log_level'],
                    file_path=global_config['log_file_path'],
                    file_colorful=False)

logger.__enter__()
logger.info("日志启动")

def log_handler(target):
    """ 添加日志运行时 """
    """ 2022年2月11日21:30:38 过期的，不应再被调用 """
    def func(*args, **kwargs) -> Any:
        logger.__enter__()
        return target(*args, **kwargs)
    return func
