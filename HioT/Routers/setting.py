from typing import Optional
from fastapi import APIRouter
from HioT.Models.device_type import ModelCreateDeviceType
from HioT.Models.response import CommonResponseModel
from HioT.Repository import setting

router = APIRouter(
    tags=["setting"],
    prefix="/setting"
)


@router.get('/devType')
def get_all_device_type(device_type_id:int=None):
    """ 获得所有设备类型及其信息 """
    return setting.get_all_device_type(device_type_id)


@router.put('/devType',response_model=CommonResponseModel)
def create_a_device_type(new_device_type:ModelCreateDeviceType):
    """ 创建一个设备类型 """
    return setting.create_a_device_type(new_device_type)


@router.delete('/devType',response_model=CommonResponseModel)
def delete_a_device_type(device_type_id:int):
    """ 删除一个设备类型 """
    return setting.delete_a_device_type(device_type_id)

@router.delete('/reset')
def reset_the_system():
    """ 危险: 重置系统 """
    return setting.reset_the_system()