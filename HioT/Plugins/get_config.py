__all__ = [
            'config',
            'global_config',
            'influxDB_config',
            'uvicorn_config',
            'mqtt_config',
            'scheduler_config'
        ]


from typing import Dict
from colorful_logger.logger import logger as default_logger
import yaml


def _load_config() -> Dict:
    """ 读取配置文件 """
    try:
        with open('./HioT.conf', 'r', encoding="utf-8") as file:
            config_raw = file.read()
    except FileNotFoundError:
        with default_logger:
            default_logger.fatal("Config file not exists.")
    return yaml.load(config_raw, yaml.FullLoader)


config: Dict = _load_config()
global_config = config['global']
influxDB_config = config['influxDB']
uvicorn_config = config['uvicorn']
mqtt_config = config['mqtt']
scheduler_config = config['scheduler']