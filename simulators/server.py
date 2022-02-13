#消息接受客户端

# import paho.mqtt.client as mqtt

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code: " + str(rc))

# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
# client.subscribe('fifa', qos=0)
# client.loop_forever() # 保持连接



import json


default_config = {
    "mq_broker":"127.0.0.1",
    "mq_port":1883,
    "hiot_server":"127.0.0.1",
    "hiot_port":8000,
    "device_type_id":2,
}

def the_mqtt(did):
    import paho.mqtt.client as mqtt
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))

    def on_message(client, userdata, msg):
        print(msg.topic)
        print(msg.payload)
        print(json.loads(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
    client.subscribe( ('fifa',0),('fidfa',0)  )
    client.loop_forever() # 保持连接

def the_work():
    #这个设备可能正在做一些别的要紧的事...返回数据，控制设备什么的
    pass

if __name__ == '__main__':
    the_mqtt(1)

    