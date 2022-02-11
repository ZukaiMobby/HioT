from fastapi import APIRouter
from HioT.Models.device import ModelDeviceChangeStatus, ModelRegisterDevice
from HioT.Models.response import CommonResponseModel
from HioT.Repository import device

router = APIRouter(
    tags=["device"],
    prefix="/device"
)

@router.get('/',response_model=CommonResponseModel)
def get_all_device():
    """ 获取所有设备id，包括所有已经注册的设备 """
    return device.get_all_device()

@router.put('/',response_model=CommonResponseModel)
def register_a_device(new_device:ModelRegisterDevice):
    """ 由设备发起，设备注册时调用 """
    return device.register_a_device(new_device)

@router.get('/{did}',response_model=CommonResponseModel)
def get_a_device_current_status(did:int):
    return device.get_a_device_current_status(did)

@router.put('/{did}',response_model=CommonResponseModel)
def change_a_device_status(new_device_info:ModelDeviceChangeStatus,did:int):
    return device.change_a_device_status(new_device_info,did)

@router.delete('/{did}',response_model=CommonResponseModel)
def delete_a_device(did:int):
    return device.delete_a_device(did)

@router.get('/{did}/stream')
def get_uri_for_streaming():
    return device.get_uri_for_streaming()

@router.get('/{did}/history',response_model=CommonResponseModel)
def get_device_history(did:int):
    return device.get_device_history(did)

@router.delete('/{did}/history')
def delete_device_history():
    return device.delete_device_history()

@router.get('/{did}/config',response_model=dict)
def device_get_config(did:int):
    """ 
    此接口由设备调用
    不是设备自身参数的设置
    """
    return device.device_get_config(did)

@router.put('/{did}/config',response_model=CommonResponseModel)
def put_device_config(did:int,new_config:dict):
    """ 
    此接口由设备所属用户调用
    说明：此处配置是设备与平台关系之间的配置
    """
    print(type(new_config))
    print(new_config)
    return device.put_device_config(did,new_config)

@router.put('/{did}/update',response_model=CommonResponseModel)
def update_device_data_item(did:int, data_item:dict):
    """ 此接口由设备调用,用来更新数据 """
    return device.update_device_data_item(did,data_item)
