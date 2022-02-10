#阶段性测试#

#新建两个用户并保存



from HioT.Models.user import ModelUser
from HioT.ModelsORM.user import add_user_to_db

user_a_info = {
    "name":"Mobby",
    "password":"lidong123",
    "privilege":0
}

user_a = ModelUser(**user_a_info)
if add_user_to_db(user_a.dict()):
    print("用户a新建成功")

user_b_info = {
    "name":"Krin",
    "password":"kris2",
    "privilege":1
}

user_b = ModelUser(**user_b_info)
if add_user_to_db(user_b.dict()):
    print("用户b新建成功")

#新建两个设备类型保存

from HioT.Models.device_type import ModelDeviceType
from HioT.ModelsORM.device_type import add_device_type_to_db

device_type_a_info = {
    "device_type_name":"Switch",
    "description":"家用智能开关",
    "data_item":{
        "volt":0.0,
        "current":0.0,
    },
    "default_config":{
        "report_interval":5,
        "on": False
    }
}

device_type_a = ModelDeviceType(**device_type_a_info)
if add_device_type_to_db(device_type_a.dict()):
    print("设备类型A新建成功")

device_type_b_info = {
    "device_type_name":"Air conditioner",
    "description":"家用空调",
    "data_item":{
        "volt":0.0,
        "current":0.0,
        "temp":0.0
    },
    "default_config":{
        "target_temp": 26,
        "report_interval":60,
        "on": False,
        "mode":"cool"
    }
}
device_type_b = ModelDeviceType(**device_type_b_info)
if add_device_type_to_db(device_type_b.dict()):
    print("设备类型B新建成功")
#每个设备类型新建两个对应的设备并保存


from HioT.ModelsORM.device_type import get_device_type_from_db_by_id
from HioT.Models.device_type import ModelDeviceType
from HioT.ModelsORM.device import add_device_to_db, update_device_config_to_db, update_device_data_item_to_db

device_1_a = {
    "device_type_id":1
}

device_1_b = {
    "device_type_id":1
}

device_2_a = {
    "device_type_id":2
}

device_2_b = {
    "device_type_id":2
}
from HioT.Models.device import ModelDevice
def gen_dev_and_add_db(info:dict):
    dev_info = get_device_type_from_db_by_id(info['device_type_id'])
    gen_dev = {
        "device_type_id" : dev_info['device_type_id'],
        "config": dev_info['default_config'],
        "data_item": dev_info['data_item']
    }
    
    dev = ModelDevice(**gen_dev)
    add_device_to_db(dev.dict())

gen_dev_and_add_db(device_1_a)
gen_dev_and_add_db(device_2_a)
gen_dev_and_add_db(device_1_b)
gen_dev_and_add_db(device_2_b)

#这4个设备更新几次数据，保存到flux

#先更新基本的状态
from HioT.ModelsORM.device import update_device_status_to_db, get_device_from_db_by_id

#********第一个设备配置
dev = ModelDevice(**get_device_from_db_by_id(1))
dev.online =True
dev.device_name = "设备1"
update_device_status_to_db(dev.dict())

dev.data_item['volt'] = 3.3
dev.data_item['current'] = 0.86

dev.config['report_interval'] = 2

update_device_config_to_db(dev.dict())
update_device_data_item_to_db(dev.dict())

#********第二个设备配置
dev = ModelDevice(**get_device_from_db_by_id(2))
dev.online =False
dev.device_name = "设备2"
update_device_status_to_db(dev.dict())

#********第四个设备配置
dev = ModelDevice(**get_device_from_db_by_id(4))
dev.online =False
dev.device_name = "设备4"
update_device_status_to_db(dev.dict())
dev.config['target_temp'] = 21
dev.config['on'] = True
dev.config['mode'] = "heat"

dev.data_item['temp'] = 16.2
update_device_config_to_db(dev.dict())
update_device_data_item_to_db(dev.dict())

#读取flux中对应的数据

# from HioT.Database.influxDB import influx_query_by_device
# print("============>1")
# influx_query_by_device(1)
# print("============>2")
# influx_query_by_device(2)
# print("============>3")
# influx_query_by_device(3)
# print("============>4")
# influx_query_by_device(4)