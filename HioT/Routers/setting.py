from fastapi import APIRouter
from HioT.Repository import setting

router = APIRouter(
    tags=["setting"],
    prefix="/setting"
)


@router.get('/devType')
def get_all_device_type():
    """ 获得所有设备类型及其信息 """
    return setting.get_all_device_type()


@router.put('/devType')
def create_a_device_type():
    """ 创建一个设备类型 """
    return setting.create_a_device_type()


@router.delete('/devType')
def delete_a_device_type():
    """ 删除一个设备类型 """
    return setting.delete_a_device_type()

@router.delete('/reset')
def reset_the_system():
    """ 危险: 重置系统 """
    return setting.reset_the_system()