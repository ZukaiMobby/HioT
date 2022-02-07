import os
import platform
from HioT.Plugins.get_config import *
from HioT.Plugins.get_logger import logger, log_handler
#需要通过调用来运行，不得单独调用

@log_handler
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


def check_for_initialize():
    check_files_db()
