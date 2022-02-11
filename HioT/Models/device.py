from typing import Optional
from pydantic import BaseModel


class ModelDevice(BaseModel):
    # 这是具体的某一个设备
    did: Optional[int]  # 设备全局唯一的设备号
    device_type_id: int  # 设备所属类型
    bind_user: Optional[int]  # 绑定的用户UID

    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述
    online: Optional[bool]  # 设备是否在线

    config: Optional[dict]  # 针对某一个设备的配置，存储时应为json
    data_item: Optional[dict]  # 设备当前的具体数值，存储时应为json


class ModelRegisterDevice(BaseModel):
    device_type_id: int  # 设备所属类型
    # device_auth_token: Optional[str] #设备认证口令，保留备用


class ModelDeviceChangeStatus(BaseModel):
    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述


if __name__ == '__main__':
    pass
