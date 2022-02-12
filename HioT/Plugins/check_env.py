from getpass import getpass
import os
from time import sleep
from HioT.Plugins.get_config import *
from HioT.Plugins.get_logger import logger

from HioT.Models.user import ModelUser
from HioT.ModelsORM.user import add_user_to_db, get_all_user_uid_from_db
import subprocess

def check_files_db():

    db_file_path = './'+global_config['database_file_path'] + \
        '/'+global_config['database_file_name']

    if not os.path.isfile(db_file_path):
        logger.warning("ORM数据库文件不存在，尝试重建...")
        os.makedirs(global_config['database_file_path'])
        with open(db_file_path, 'w', encoding='utf-8'):
            pass
        logger.info("ORM数据库文件新建完成！")

    else:
        logger.debug("找到数据库文件")


def startup():
    mos = subprocess.Popen(r"Env\mosquitto\mosquitto.exe")
    influx = subprocess.Popen(r"Env\influxdb\influxd.exe")


def is_first_run():
    #检查用户列表是否为空来判断是否第一次运行
    u_res = get_all_user_uid_from_db()
    empty_res = []
    if u_res == empty_res:
        return True
    else:
        return False

def rebuild_env():
    #用于重置环境
    db_file_path = './'+global_config['database_file_path'] + \
        '/'+global_config['database_file_name']

    if not os.path.isfile(db_file_path):
        logger.info("ORM数据库文件不存在，无法删除...")

    os.remove(db_file_path)
    logger.info("ORM数据库文件删除指令已下达")

    p = subprocess.Popen(r"Env\influxdb\influxd.exe")
    sleep(5)

    del_command = f"Env\influxdb\influx.exe bucket delete --name {influxDB_config['bucket']} --org {influxDB_config['org']} --token {influxDB_config['token']}"
    process = subprocess.Popen(del_command)
    logger.info("influx bucket 删除指令已下达")
    process.wait()
    create_command = f"Env\influxdb\influx.exe bucket create --name {influxDB_config['bucket']} --org {influxDB_config['org']} --token {influxDB_config['token']}"
    subprocess.Popen(create_command)
    logger.info("influx bucket 创建指令已下达")
    process.wait()

    p.kill()


def check_for_initialize():
    check_files_db()  # 检查文件完整性
    if is_first_run():
        print("欢迎使用HioT,让我们开始吧")
        print("这似乎是您第一次运行，让我们知道您是谁~")
        name = input("请输入用户名：")
        password = getpass("为确保账号安全，请输入密码：")
        new_user = ModelUser(name=name,password=password,privilege=2)
        if not add_user_to_db(new_user.dict()):
            logger.fatal("初始化第一个用户时发生错误，请检查..")
        print("您的UID为 1, UID是平台识别账号的唯一凭据")
        print("5秒后继续...")
        sleep(5)
    try:
        startup()
    except:
        logger.fatal("一个或多个组件无法启动..")
    
    

if __name__ == '__main__':
    #rebuild_env()
    pass