from ipaddress import IPv4Address, IPv6Address
from typing import Optional
from pydantic import BaseModel, PositiveInt

p_mqtt = 1
p_ipv4 = 2
p_ipv6 = 3

class ModelDevice(BaseModel):
    # 这是具体的某一个设备
    did: Optional[int]  # 设备全局唯一的设备号
    device_type_id: int  # 设备所属类型
    bind_user: Optional[int]  # 绑定的用户UID

    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述

    online: Optional[bool]  # 设备是否在线
    keep_alive:Optional[int] # 超过这段时间没有通信过判为失活

    ipv4: Optional[IPv4Address] #IPV4 地址支持(实际上是int)
    v4port: Optional[PositiveInt] #IPV4 通信端口(还是int)

    ipv6: Optional[IPv6Address] #IPV6 地址支持(实际还是int)
    v6port: Optional[PositiveInt] #IPV6 通信端口(还是int)

    protocol:Optional[int] #设备选择的协议

    config: Optional[dict]  # 针对某一个设备的配置，存储时应为json
    data_item: Optional[dict]  # 设备当前的具体数值，存储时应为json


class ModelRegisterDevice(BaseModel):
    device_type_id: int  # 设备所属类型
    # device_auth_token: Optional[str] #设备认证口令，保留备用


class ModelDeviceChangeStatus(BaseModel):
    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述
    keep_alive: Optional[int]
    v4port:Optional[int]
    v6port:Optional[int]
    protocol:Optional[int]



if __name__ == '__main__':
    pass
