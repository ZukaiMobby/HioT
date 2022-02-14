from HioT.Models.user import ModeUserInfoDisplay, ModelUpdateUser, ModelUser
from HioT.ModelsORM.user import delete_user_from_db, get_all_user_uid_from_db,add_user_to_db, get_user_from_db_by_id, update_user_to_db

def get_all_users():
    return get_all_user_uid_from_db()

def create_a_user(new_user_info):
    new_user = ModelUser(**new_user_info.dict())
    result = add_user_to_db(new_user.dict())
    response = {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }
    return response

def query_a_user(uid:int):
    user_info = get_user_from_db_by_id(uid)
    if user_info == {}:
        return {
            "errno":402,
            "message":"用户不存在",
            "data":{}
        }

    user = ModeUserInfoDisplay(**user_info)

    response = {
        "errno":0,
        "message":"查询成功",
        "data":user.dict()
    }

    return response

def delete_a_user(uid:int):
    result = delete_user_from_db(uid)
    return {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }

def modify_a_user(uid:int,update_user_info:ModelUpdateUser):

    user_info = get_user_from_db_by_id(uid)
    if user_info == {}:
        return {
            "errno":402,
            "message":f"用户 {uid} 不存在",
            "data":{}
        }

        
    the_user = ModelUser(**user_info)
    for k,v in update_user_info.dict().items():
        if k == 'password':
            the_user.password = v
        elif k == 'name':
            the_user.name = v
        else:
            pass
    result = update_user_to_db(the_user.dict())

    response = {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }
    return response


def get_user_devices_did(uid:int):
    user_info = get_user_from_db_by_id(uid)

    if user_info == {}:
        return {
        "errno":0,
        "message":f"用户 {uid} 不存在",
        "data":{}
        }

    the_user = ModelUser(**user_info)
    return {
        "errno":0,
        "message":f"用户 {the_user.uid} 设备列表",
        "data":the_user.devices
    }


def add_a_device_to_user(uid:int,did:int):

    user_info = get_user_from_db_by_id(uid)
    if not user_info:
        return {
            "errno":402,
            "message":f"添加设备至用户 {uid} 时：用户查询接口返回空",
            "data":{}
        }
    
    the_user = ModelUser(**user_info)
    result = the_user.bind_device(did)

    response = {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }
    return response

def delete_a_device_from_user(uid:int,did:int):
    user_info = get_user_from_db_by_id(uid)
    if user_info == {}:
        return {
            "errno":402,
            "message":f"用户 {uid} 不存在",
            "data":{}
        }
    
    the_user = ModelUser(**user_info)
    result = the_user.unbind_device(did)

    response = {
        "errno":result[1],
        "message":result[2],
        "data":result[3]
    }
    return response
