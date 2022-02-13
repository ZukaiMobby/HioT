import ipaddress
from starlette.requests import Request
from HioT.Database.influxDB import influx_query_by_device
from HioT.Models.device import ModelDevice, ModelDeviceChangeStatus, ModelRegisterDevice
from HioT.Models.user import ModelUser
from HioT.ModelsORM.device import add_device_to_db, delete_device_from_db, get_all_device_did, get_device_from_db_by_id, update_device_config_to_db, update_device_data_item_to_db, update_device_status_to_db
from HioT.ModelsORM.device_type import get_device_type_from_db_by_id
from HioT.ModelsORM.user import get_user_from_db_by_id

def get_all_device():
    """ 获取所有设备id，包括所有已经注册的设备 """
    return {
        "errno":0,
        "message":f"设备did列表",
        "data":get_all_device_did()
    }


def register_a_device(new_device_info: ModelRegisterDevice,request:Request):
    """ 由设备发起，设备注册时调用 """
    ip:str = request.client[0]
    ip = ipaddress.ip_address(ip)
    port:int = request.client[1]

    if type(ip) == ipaddress.IPv4Address:
        is_v4 = True
    else:
        is_v4 = False

    def gen_dev_and_add_db(new_device_info:ModelRegisterDevice):

        dev_info = get_device_type_from_db_by_id(new_device_info.device_type_id)

        if dev_info == {}:
            return {
                "errno":403,
                "message": f"设备类型 {new_device_info.device_type_id} 不存在",
                "data":{}
                }

        if is_v4:
            gen_dev = {
                "device_type_id" : dev_info['device_type_id'],
                "keep_alive":dev_info['keep_alive'],
                "ipv4":int(ipaddress.IPv4Address(ip)),
                "v4port":dev_info['v4port'],
                "protocol":dev_info['protocol'],
                "config": dev_info['default_config'],
                "data_item": dev_info['data_item'],
            }
        else:
            gen_dev = {
                "device_type_id" : dev_info['device_type_id'],
                "keep_alive":dev_info['keep_alive'],
                "ipv6":int(ipaddress.IPv6Address(ip)),
                "v6port":dev_info['v6port'],
                "protocol":dev_info['protocol'],
                "config": dev_info['default_config'],
                "data_item": dev_info['data_item'],
            }
        
        dev = ModelDevice(**gen_dev)
        
        return add_device_to_db(dev.dict())
    result = gen_dev_and_add_db(new_device_info)
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }


def get_a_device_current_status(did:int):
    the_deivce_info = get_device_from_db_by_id(did)
    if the_deivce_info == {}:
        return {
            "errno":401,
            "message": f"设备{did}查询失败，接口返回了空",
            "data":{}
            }

    the_device = ModelDevice(**the_deivce_info)
    return {
        "errno":0,
        "message": f"设备{did}当前信息",
        "data":the_device.dict()
    }


def change_a_device_status(new_device_status_info:ModelDeviceChangeStatus,did:int):
    device_info = get_device_from_db_by_id(did)
    if device_info == {}:
        return {
            "errno":401,
            "message": f"修改设备{did}查询失败，接口返回了空",
            "data":{}
            }

    the_device = ModelDevice(**device_info)

    for k,v in new_device_status_info.dict().items():
        if k == 'device_name':
            the_device.device_name = v
        elif k == 'device_description':
            the_device.device_description = v

        elif k == 'keep_alive' and v :
            the_device.keep_alive = int(v)

        elif k == 'v4port' and v :
            the_device.v4port = int(v)
        
        elif k == 'v6port' and v:
            the_device.v6port = int(v)

        elif k == 'protocol' and v:
            the_device.protocol = int(v)

        else:
            pass
    result = update_device_status_to_db(the_device.dict())
    
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }

def delete_a_device(did:int):
    the_device_info = get_device_from_db_by_id(did)

    if the_device_info == {}:
        return {
            "errno":401,
            "message": f"设备{did}查询失败，接口返回了空",
            "data":{}
            }

    the_device = ModelDevice(**the_device_info)
    user_info = get_user_from_db_by_id(the_device.bind_user)
    if user_info == {}:
        return{
            "errno":400,
            "message":f"设备 {did} 绑定了一个不存在的用户 {the_device.bind_user} ",
            "data":{}
        }

    the_user = ModelUser(**user_info)
    result = the_user.unbind_device(did)

    if result[0] == False:
        return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }

    else:
        result = delete_device_from_db(did)
        return {
            "errno":result[1],
            "message":result[2],
            "data":result[3]
    }


def get_uri_for_streaming():
    return "正在开发中..."

def get_device_history(did:int):
    return {
        "errno":0,
        "message":"Device history data",
        "data":{
            "records":influx_query_by_device(did)
        }
    }

def delete_device_history():
    return "此接口暂不考虑开发"
    pass

def device_get_config(did:int):
    """ 此接口由设备调用 """
    device_info = get_device_from_db_by_id(did)
    if device_info == {}:
        return {}
    the_device = ModelDevice(**device_info)
    return the_device.config

def put_device_config(did:int,new_config):
    """ 此接口由设备所属用户调用,建议从查询接口获得原来的配置之后修改 """
    device_info = get_device_from_db_by_id(did)
    if device_info == {}:
        return {
            "errno":401,
            "message": f"设备{did}查询失败，接口返回了空",
            "data":{}
        }
        
    the_device = ModelDevice(**device_info)
    the_device.config = new_config
    result = update_device_config_to_db(the_device.dict())
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }

def update_device_data_item(did:int,data_item:dict,request):
    
    print(data_item)

    device_info = get_device_from_db_by_id(did)
    if device_info == {}:
        return {
            "errno":401,
            "message": f"设备{did}查询失败，接口返回了空",
            "data":{}
        }
        
    the_device = ModelDevice(**device_info)
    the_device.data_item = data_item
    result = update_device_data_item_to_db(the_device.dict())
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }
