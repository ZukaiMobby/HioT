from HioT.Models.device_type import ModelCreateDeviceType, ModelDeviceType
from HioT.ModelsORM.device_type import add_device_type_to_db, delete_device_type_from_db, get_all_device_type_from_db, get_device_type_from_db_by_id


def get_all_device_type(device_type_id):
    """ 获得所有设备类型及其信息 """

    if device_type_id != None:
        res = get_device_type_from_db_by_id(device_type_id)
        if res != {}:
            return res
        else:
            return{}
    else:
        res = get_all_device_type_from_db()
        return_list = []
        if len(res)!=0:
            for tid in res:
                return_list.append(get_device_type_from_db_by_id(tid))
    return return_list


def create_a_device_type(new_device_type:ModelCreateDeviceType):
    """ 创建一个设备类型 """
    device_type = ModelDeviceType(**new_device_type.dict())
    result = add_device_type_to_db(device_type.dict())
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }


def delete_a_device_type(device_type_id:int):
    """ 删除一个设备类型 """
    result = delete_device_type_from_db(device_type_id)
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }

def reset_the_system():
    """ 危险: 重置系统 """
    pass