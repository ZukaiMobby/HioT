# RUN TIME ENV CHECK

# 检查数据库文件夹及文件是否存在
# 不存在则新建
import os
import platform
from typing import Dict

import influxdb_client
import yaml
import uvicorn
from colorful_logger.logger import get_logger
from colorful_logger.logger import logger as default_logger
from rich import print
from fastapi import FastAPI

app = FastAPI()


def load_config() -> Dict:
    """ 读取配置文件 """
    try:
        with open('./config.yaml', 'r', encoding="utf-8") as file:
            config_raw = file.read()
    except FileNotFoundError:
        with default_logger:
            default_logger.fatal("Config file not exists.")
    return yaml.load(config_raw, yaml.FullLoader)


def check_files_db():
    """ 检查数据库文件 """
    db_file_path = './'+global_config['database_file_path'] + \
        '/'+global_config['database_file_name']
    if not os.path.isfile(db_file_path):
        os.makedirs(global_config['database_file_path'])
        with open(db_file_path, 'w', encoding='utf-8'):
            logger.warning("数据库文件不存在")
    else:
        logger.debug("找到数据库文件")

def check_influxdb():
    """ 检查influxdb 连接性 """
    # sys_platform = platform.uname()
    # sys_platform = sys_platform[0]
    # if sys_platform == 'Windows':
    #     os.startfile(influxDB_config['path']+"\influxd.exe")

    # client = influxdb_client.InfluxDBClient(
    #     url='http://'+influxDB_config['host']+':'+influxDB_config['port'], token='')
    # print(client.get_list_database())

if __name__ == '__main__':
    config: Dict = load_config()
    global_config = config['global']
    influxDB_config = config['influxDB']
    uvicorn_config = config['uvicorn']

    # 初始化日志器
    logger = get_logger(name="main_logger",
                        level=global_config['log_level'],
                        file_path=global_config['log_file_path'],
                        file_colorful=False)

    with logger:
        logger.debug("配置文件获取成功")

        # 检查数据库
        check_files_db()

        # 拉起InfluxDB及连接性检查
        # check_influxdb()

    # FastAPI 配置
    

    

    uvicorn.run("main:app", 
        host=uvicorn_config['host'], 
        port=uvicorn_config['port'],
        log_level='info')