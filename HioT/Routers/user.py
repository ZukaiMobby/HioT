from typing import List
from fastapi import APIRouter
from HioT.Models.response import CommonResponseModel
from HioT.Models.user import ModelNewUser, ModelUpdateUser, ModelUser
from HioT.Repository import user

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.get('/', response_model=List[int])
def get_all_users():
    #DEV:1.0
    #OK: [1,2,3...]
    return user.get_all_users()

@router.post('/',status_code=201,response_model=CommonResponseModel)
def create_a_user(new_user_info:ModelNewUser):
    #DEV：1.0
    return user.create_a_user(new_user_info)

@router.get('/{uid}',response_model=CommonResponseModel)
def query_a_user(uid:int):
    return user.query_a_user(uid)

@router.put('/{uid}')
def modify_a_user(uid,update_user_info:ModelUpdateUser):
    return user.modify_a_user(uid,update_user_info)

@router.delete('/{uid}/',response_model=CommonResponseModel)
def delete_a_user(uid):
    return user.delete_a_user(uid)

@router.get('/{uid}/device',response_model=CommonResponseModel)
def get_user_devices_did(uid):
    return user.get_user_devices_did(uid)

@router.post('/{uid}/device',response_model=CommonResponseModel)
def add_a_device_to_user(uid,did:int):
    return user.add_a_device_to_user(uid,did)

@router.delete('/{uid}/device',response_model=CommonResponseModel)
def delete_a_device_from_user(uid:int,did:int):
    return user.delete_a_device_from_user(uid,did)