from time import sleep
from HioT.Plugins.get_config import *
from HioT.Plugins.get_logger import logger

from HioT.Models.user import ModelUser
from HioT.ModelsORM.user import add_user_to_db, get_all_user_uid_from_db


def check_orm_database() -> bool:
    import os
    db_file_path = './'+global_config['database_file_path'] +'/'+global_config['database_file_name']

    try:
        with open(db_file_path) as f:
            logger.info("ORM数据库文件存在")
            return True
    except FileNotFoundError:
        logger.warning("ORM 数据库文件不存在，尝试重建...")
        os.makedirs(global_config['database_file_path'])
        with open(db_file_path, 'w', encoding='utf-8'):
            pass
        logger.info("ORM数据库文件新建完成！")
        return True
    except PermissionError:
        logger.error("进程无法访问，或许另一个程序正在使用")
        return False

def is_mosquitto_alive() -> bool:
    import paho.mqtt.client as mqtt
    from HioT.Plugins.get_config import mqtt_config

    flag = None
    def on_connect(client, userdata, flags, rc):
        nonlocal flag
        flag = True
        return


    client = mqtt.Client() #拿到instance
    client.connect(mqtt_config['host'],mqtt_config['port'],mqtt_config['keepalive'] ) # 600为keepalive的时间间隔
    client.on_connect = on_connect
    client.loop()
    return flag

def is_influx_alive() -> bool:
    import requests
    from HioT.Plugins.get_config import influxDB_config
    url = influxDB_config['url']+'/ping'
    try:
        res = requests.get(url)
        if res.status_code == 204:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


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
    import os
    import subprocess
    logger.error("重置函数已经不再使用..")

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

def init_for_first_run():
    from getpass import getpass
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    print("欢迎使用HioT,让我们开始吧")
    print("这似乎是您第一次运行，让我们知道您是谁~")
    name = input("请输入用户名：")
    password = getpass("为确保账号安全，请输入密码：")
    pwd_hashed = pwd_context.hash(password)
    print(pwd_hashed)
    new_user = ModelUser(name=name,password=pwd_hashed,privilege=2)
    if not add_user_to_db(new_user.dict()):
        logger.fatal("初始化第一个用户时发生错误，请检查..")
    print("您的UID为 1, UID是平台识别账号的唯一凭据")
    print("5秒后继续...")
    sleep(5)
    pass

def check_for_initialize():
    
    ok = True

    if not check_orm_database():
        logger.error("sqlite 连接失败...")
        ok = False
    if not is_influx_alive():
        logger.error("INFUX DB 连接失败...")
        ok = False
    if not is_mosquitto_alive():
        logger.error("mosquitto 连接失败...")
        ok = False
    if not ok:
        logger.fatal("一个或多个组件连接失败，继续启动可能导致数据丢失")

    if is_first_run():
        init_for_first_run()



if __name__ == '__main__':
    init_for_first_run()
    pass