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
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
    client.subscribe('fifa', qos=0)
    client.loop_forever() # 保持连接

def the_work():
    #这个设备可能正在做一些别的要紧的事...返回数据，控制设备什么的
    pass

if __name__ == '__main__':
    print("我是空调，要和服务器建立初次连接，我现在要初试配置")
    print("有了配置我需要连接")
    ##########以下内容需要通过FASTAPI接口完成###################
    
    from HioT.Models.device import ModelDevice
    from HioT.ModelsORM.device_type import get_device_type_from_db_by_id
    from HioT.ModelsORM.device import add_device_to_db

    def gen_dev_and_add_db(info:dict):
        dev_info = get_device_type_from_db_by_id(info['device_type_id'])
        gen_dev = {
            "device_type_id" : dev_info['device_type_id'],
            "config": dev_info['default_config'],
            "data_item": dev_info['data_item']
        }
        dev = ModelDevice(**gen_dev)
        add_device_to_db(dev.dict())
        return dict

    config = gen_dev_and_add_db(default_config) #初次连接需要从服务器获得配置信息

    ##########以上内容需要通过FASTAPI接口完成###################

    #有了从服务器获得的配置信息，就可以进行相关推送了

    #比方说我设备在config里获得我的设备ID是4，通信方式是MQTT



    