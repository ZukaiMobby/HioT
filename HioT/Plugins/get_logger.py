from typing import Any
from colorful_logger.logger import get_logger
from HioT.Plugins.get_config import global_config

logger = get_logger(name="main",
                    level=global_config['log_level'],
                    file_path=global_config['log_file_path'],
                    file_colorful=False)


def log_handler(target):
    """ 添加日志运行时 """
    """ 原来函数有什么我就返回什么 """
    def func(*args, **kwargs) -> Any:
        with logger:
            return target(*args, **kwargs)

    return func
