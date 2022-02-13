import json
import random
from time import sleep
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    #定义实践调用函数
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# p = {
#     "ee":"we"
# }

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
# client.publish('fifa', payload=json.dumps(p), qos=0)

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

def work():
    pass

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
    client.connect('127.0.0.1', 1883, 30)
    temp = random.uniform(30.1,66.4)
    humi = random.uniform(50.1,96.4)
    while True:
        temp = random.uniform(30.1,66.4)
        humi = random.uniform(50.1,96.4)
        client.publish(from_server_config['publish_topic'], 
        payload=json.dumps({"temp":temp,"humi":humi}), qos=0)
        sleep(10)
