
import paho.mqtt.client as mqtt


from HioT.Plugins.get_config import mqtt_config

def on_connect(client, userdata, flags, rc):
    print(f"MQTT Broker connention result:{str(rc)}")

def on_message(client, userdata, msg):
    pass

client = mqtt.Client() #拿到instance
client.connect(mqtt_config['host'],mqtt_config['port'],mqtt_config['keepalive'] ) # 600为keepalive的时间间隔
client.on_connect = on_connect
client.on_message = on_message
# client.subscribe(subscribe_list)
#client.on_connect_fail  这个参数可以指定一下
client.loop_forever()