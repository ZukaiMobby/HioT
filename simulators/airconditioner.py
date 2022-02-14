import json
import random
from time import sleep
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    #定义实践调用函数
    print("Connected with result code: " + str(rc))

temp = 0.0
humi = 0.0

default_sever_config = {
    "broker": "127.0.0.1",
    "bport": 1883,
}

from_server_config = {}

device_config = {
    "refresh": 10,
    "target_temp": 26.0,
    "on": False
}

reg_info = {"device_type_id": 1}

import requests
url = "http://127.0.0.1:8001/device/"

def register():
    global from_server_config
    r = requests.put(url, data=json.dumps(reg_info))
    result = json.loads(r.content)
    from_server_config = result['data']

    with open("config.pkl","wb") as f:
        pickle.dump(from_server_config,f)


def on_message(client, userdata, msg):
    global device_config
    if msg.payload:
        try:
            config:dict = json.loads(msg.payload)
        except json.JSONDecodeError:
            print("收到了不可解析的json数据")
            return

    device_config = config

    from rich import print
    print("新的配置数据")
    print(device_config)


if __name__ == '__main__':
    from rich import print
    print("模拟空调设备...启动中")
    print("加载配置文件...")

    import pickle

    try:
        with open("config.pkl","rb") as f:
            from_server_config = pickle.load(f)
    except FileNotFoundError:
        pass
    
    if from_server_config == {}:
        register()
        print(from_server_config)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('127.0.0.1', 1883, 600)
    client.subscribe(from_server_config['subscribe_topic'],0)
    print(f"订阅配置推送：{from_server_config['subscribe_topic']}")
    
    temp = random.uniform(30.1,66.4)
    humi = random.uniform(50.1,96.4)
    client.loop_start()

    while True:
        temp = random.uniform(30.1,66.4)
        humi = random.uniform(50.1,96.4)
        client.publish(from_server_config['publish_topic'], 
        payload=json.dumps({"temp":temp,"humi":humi}), qos=0)
        print("推送了数据")
        sleep(10)
