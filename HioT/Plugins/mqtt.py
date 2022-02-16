import json
from types import NoneType
from typing import List, Tuple
import paho.mqtt.client as mqtt


from HioT.ModelsORM.device import get_device_from_db_by_id, update_device_data_item_to_db
from HioT.Plugins.get_logger import logger
from HioT.Plugins.get_config import mqtt_config
from HioT.Database.sqliteDB import engine


with engine.connect() as con:
    res = con.execute('SELECT did from Device where protocol == 1')
    if type(res) == NoneType:
        device_list = []
    else:
        #这里的Item[0] 实际就是did号
        subscribe_list = [ (f'did{item[0]}publish',0) for item in res ]


def on_connect(client, userdata, flags, rc):
    logger.info(f"MQTT Broker connention result:{str(rc)}")

def on_message(client, userdata, msg):
    topic:str = msg.topic
    topic = topic.removeprefix('did')
    topic = topic.removesuffix('publish')
    did:int = int(topic)
    data:str = msg.payload

    if not data:
        pass
    else:
        try:
            data_item = json.loads(data)
            receive_data_from_device(did,data_item)
        except json.JSONDecodeError:
            #判断是不是遗嘱信息
            data = data.removeprefix('did')
            data = data.removesuffix('offline')
            try:
                did = int(data)
                receive_will_message(did)
            except ValueError:
                logger.error("收到不可反序列化JSON")


client = mqtt.Client() #拿到instance
client.connect(mqtt_config['host'],mqtt_config['port'],mqtt_config['keepalive'] )
client.on_connect = on_connect
client.on_message = on_message
client.subscribe(subscribe_list)
client.loop_start()

def receive_data_from_device(did:int,data_item:dict) -> Tuple[bool,int,str,dict]:
    from HioT.Models.device import ModelDevice
    from rich import print


    device_info = get_device_from_db_by_id(did)
    if not device_info:
        logger.error(f"处理MQTT错误：查询设备{did}时接口返回空")

    dev = ModelDevice(**device_info)
    dev.data_item = data_item
    dev.set_device_online()
    return update_device_data_item_to_db(dev.dict())

def receive_will_message(did:int):
    from HioT.Models.device import ModelDevice
    device_info = get_device_from_db_by_id(did)
    if not device_info:
        logger.error(f"处理MQTT遗嘱错误：查询设备{did}时接口返回空")
    dev = ModelDevice(**device_info)
    dev.set_device_offline()

def push_config_to_device(did:int,config:dict):
    try:
        config = json.dumps(config)
        client.publish(f'did{did}subscribe', payload=config, qos=0)
        logger.info(f"推送设备{did}配置完成")
    except json.JSONDecodeError:
        logger.error(f"处理MQTT错误：推送设备{did}配置时JSON无法序列化")
    

def add_new_dev_to_subscribe(did):
    client.subscribe(f'did{did}publish', qos=0)

def remove_dev_from_subscribe(did):
    client.unsubscribe(f'did{did}publish')
