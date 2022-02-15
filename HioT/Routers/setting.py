from typing import Optional
from fastapi import APIRouter, Depends
from HioT.Models.device_type import ModelCreateDeviceType
from HioT.Models.response import CommonResponseModel
from HioT.Repository import setting
from HioT.Security.utils import ROOT, gen_operation_privilige, get_current_user_by_token,privilige_exception

router = APIRouter(
    tags=["setting"],
    prefix="/setting"
)


@router.get('/devType')
def get_all_device_type(request_user = Depends(get_current_user_by_token),device_type_id:int=None):
    """ 获得所有设备类型及其信息 """
    API_PRIVILIGE = ROOT
    if gen_operation_privilige(request_user) > API_PRIVILIGE:
        raise privilige_exception
    return setting.get_all_device_type(device_type_id)


@router.put('/devType',response_model=CommonResponseModel)
def create_a_device_type(new_device_type:ModelCreateDeviceType,request_user = Depends(get_current_user_by_token)):
    """ 创建一个设备类型 """
    API_PRIVILIGE = ROOT
    if gen_operation_privilige(request_user) > API_PRIVILIGE:
        raise privilige_exception
    return setting.create_a_device_type(new_device_type)


@router.delete('/devType',response_model=CommonResponseModel)
def delete_a_device_type(device_type_id:int,request_user = Depends(get_current_user_by_token)):
    """ 删除一个设备类型 """
    API_PRIVILIGE = ROOT
    if gen_operation_privilige(request_user) > API_PRIVILIGE:
        raise privilige_exception
    return setting.delete_a_device_type(device_type_id)

# @router.delete('/reset')
# def reset_the_system():
#     """ 危险: 重置系统 """
#     return setting.reset_the_system()