from colorful_logger.logger import get_logger
from HioT.Plugins.get_config import global_config

logger = get_logger(name="main_logger",
                    level=global_config['log_level'],
                    file_path=global_config['log_file_path'],
                    file_colorful=False)


def log_handler(target):
    """ 添加日志运行时 """
    def func(*args, **kwargs):
        with logger:
            target()
    return func
