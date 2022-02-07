from fastapi import APIRouter
from HioT.Repository import device

router = APIRouter(
    tags=["device"],
    prefix="/device"
)

@router.get('/')
def get_all_device():
    """ 获取所有设备id，包括所有已经注册的设备 """
    return device.get_all_device()

@router.put('/')
def register_a_device():
    """ 由设备发起，设备注册时调用 """
    return device.register_a_device()

@router.get('/{did}')
def get_a_device_current_status():
    return device.get_a_device_current_status()

@router.put('/{did}')
def change_a_device_status():
    return device.change_a_device_status()

@router.delete('/{did}')
def delete_a_device():
    return device.delete_a_device()

@router.get('/{did}/stream')
def get_uri_for_streaming():
    return device.get_uri_for_streaming()

@router.get('/{did}/history')
def get_device_history():
    return device.get_device_history()

@router.delete('/{did}/history')
def delete_device_history():
    return device.delete_device_history()

@router.get('/{did}/config')
def device_get_config():
    """ 
    此接口由设备调用
    说明：此处配置是设备与平台关系之间的配置
    不是设备自身参数的设置
    """
    return device.device_get_config()

@router.put('/{did}/config')
def put_device_config():
    """ 
    此接口由设备所属用户调用
    说明：此处配置是设备与平台关系之间的配置
    """
    return device.put_device_config()

