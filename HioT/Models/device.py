from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Optional
from pydantic import BaseModel, PositiveInt
from HioT.ModelsORM.device import update_device_status_to_db

p_mqtt = 1
p_ipv4 = 2
p_ipv6 = 3

class ModelDevice(BaseModel):
    # 这是具体的某一个设备
    # 一些功能的安排：
    """
    config 里面用户可以自行添加数据的推送周期
    推送接口是 /device/{did}/update

    keep_alive 是设备的失活时间，单位秒（整形）
    在JSON中：如果平台发现设备距离上一次推送超过了这个时间，那么判断为失效，更新online状态

    在MQTT中 keep_alive 就是MQTT的 keepalive
    
    """
    did: Optional[int]  # 设备全局唯一的设备号
    device_type_id: int  # 设备所属类型
    bind_user: Optional[int]  # 绑定的用户UID

    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述

    online: Optional[bool]  # 设备是否在线
    keep_alive:Optional[PositiveInt] # 超过这段时间没有通信过判为失活

    ipv4: Optional[IPv4Address] #IPV4 地址支持(实际上是int)
    v4port: Optional[PositiveInt] #IPV4 通信端口(还是int)

    ipv6: Optional[IPv6Address] #IPV6 地址支持(实际还是int)
    v6port: Optional[PositiveInt] #IPV6 通信端口(还是int)

    protocol:Optional[int] #设备选择的协议

    last_vist: Optional[datetime]  #设备最后一次访问平台
    config: Optional[dict]  # 针对某一个设备的配置，存储时应为json
    data_item: Optional[dict]  # 设备当前的具体数值，存储时应为json

    def check_online(self) -> bool:
        # 返回设备状态是否变化
        now = datetime.timestamp(datetime.now())
        if now - datetime.timestamp(self.last_vist) > self.keep_alive and self.online:
            self.set_device_offline()
            return True
        elif now - datetime.timestamp(self.last_vist) < self.keep_alive and not self.online:
            self.set_device_online()
            return True
        else:
            return False

    def set_device_online(self):
        self.online = True
        return update_device_status_to_db(self.dict())

    def set_device_offline(self):
        self.online = False
        return update_device_status_to_db(self.dict())
        

class ModelRegisterDevice(BaseModel):
    device_type_id: int  # 设备所属类型
    # device_auth_token: Optional[str] #设备认证口令，保留备用


class ModelDeviceChangeStatus(BaseModel):
    device_name: Optional[str]  # 设备名称
    device_description: Optional[str]  # 设备描述
    keep_alive: Optional[PositiveInt]
    v4port:Optional[PositiveInt]
    v6port:Optional[PositiveInt]
    protocol:Optional[int]



if __name__ == '__main__':
    pass
