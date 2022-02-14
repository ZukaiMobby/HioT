def pub_str_gen(did) -> str:
    return f"did{did}publish"


def sub_str_gen(did) -> str:
    return f"did{did}subscribe"

"""

这个是平台端，不要脑袋瓜子写糊涂了！！！！

"""

import json
from typing import List, Tuple
import paho.mqtt.client as mqtt


from HioT.ModelsORM.device import get_all_device_did, get_device_from_db_by_id, update_device_data_item_to_db
from HioT.Plugins.get_logger import logger
from HioT.Plugins.get_config import mqtt_config

#启动第一步，读取协议为1的设备DID以订阅！！
#这一步应该在在导入的时候完成，并且不能被阻塞，使得导入顺利完成
device_list = get_all_device_did()
mqtt_dev_list = []

for did in device_list:
    dev:dict = get_device_from_db_by_id(did)
    if dev['protocol'] == 1:
            mqtt_dev_list.append(did)

subscribe_list = [ (f'did{did}publish',0) for did in mqtt_dev_list ]

#拿到了设备列表，那么就开始订阅/推送

def on_connect(client, userdata, flags, rc):
    logger.info(f"MQTT Broker connention result:{str(rc)}")

def on_message(client, userdata, msg):
    topic:str = msg.topic
    topic = topic.removeprefix('did')
    topic = topic.removesuffix('publish')
    did = int(topic)
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
client.connect(mqtt_config['host'],mqtt_config['port'],mqtt_config['keepalive'] ) # 600为keepalive的时间间隔
client.on_connect = on_connect
client.on_message = on_message
client.subscribe(subscribe_list)
#client.on_connect_fail  这个参数可以指定一下


client.loop_start()

def receive_data_from_device(did:int,data_item:dict) -> Tuple[bool,int,str,dict]:
    from HioT.Models.device import ModelDevice
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
