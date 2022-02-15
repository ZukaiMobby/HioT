from datetime import timedelta
from types import NoneType
from fastapi import HTTPException,status
from HioT.Models.user import ModeUserInfoDisplay, ModelUpdateUser, ModelUser
from HioT.ModelsORM.user import delete_user_from_db, get_all_user_uid_from_db,add_user_to_db, get_user_from_db_by_id, update_user_to_db
from HioT.Security.utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, pwd_context
from fastapi.security import OAuth2PasswordRequestForm


def get_all_users():
    return get_all_user_uid_from_db()

def create_a_user(new_user_info):
    new_user = ModelUser(**new_user_info.dict())
    new_user.password = pwd_context.encrypt(new_user.password)
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
            the_user.password = pwd_context.encrypt(v)
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

def login_get_token(form_data: OAuth2PasswordRequestForm):
    if form_data.username:
        try:
            uid:str = form_data.username #subject must be a string
            pwd:str = form_data.password
            user: ModelUser = authenticate_user(int(uid),pwd)

            if type(user) == NoneType:
                raise HTTPException(
                    status_code=401,
                    detail = "Incorrect uid or password",
                    headers = {"WWW-Authenticate": "Bearer"},)
            else:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(data={"sub": uid}, expires_delta=access_token_expires)
                return {"access_token": access_token, "token_type": "bearer"}
        except ValueError:
            raise HTTPException(
                status_code = 422,
                detail = "Incorrect uid: Username should enter uid",
                headers = {"WWW-Authenticate": "Bearer"},)