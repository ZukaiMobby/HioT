import imp
from lib2to3.pgen2 import token
from typing import List
from fastapi import APIRouter, Depends
from HioT.Models.response import CommonResponseModel
from HioT.Models.user import ModelNewUser, ModelUpdateUser, ModelUser
from fastapi.security import OAuth2PasswordRequestForm
from HioT.Security.models import Token
from HioT.Security.utils import get_current_user_by_token, oauth2_scheme
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

@router.post('/login', response_model=Token)
def login_get_token(form: OAuth2PasswordRequestForm = Depends()):
    return user.login_get_token(form)


@router.get('/{uid}',response_model=CommonResponseModel)
def query_a_user(uid:int,request_user = Depends(get_current_user_by_token)):
    if not request_user:
        print("用户未登入")
        return
    return user.query_a_user(uid)

@router.put('/{uid}')
def modify_a_user(uid:int,update_user_info:ModelUpdateUser):
    return user.modify_a_user(uid,update_user_info)

@router.delete('/{uid}/',response_model=CommonResponseModel)
def delete_a_user(uid:int):
    return user.delete_a_user(uid)

@router.get('/{uid}/device',response_model=CommonResponseModel)
def get_user_devices_did(uid:int):
    return user.get_user_devices_did(uid)

@router.post('/{uid}/device',response_model=CommonResponseModel)
def add_a_device_to_user(uid:int,did:int):
    return user.add_a_device_to_user(uid,did)

@router.delete('/{uid}/device',response_model=CommonResponseModel)
def delete_a_device_from_user(uid:int,did:int):
    return user.delete_a_device_from_user(uid,did)