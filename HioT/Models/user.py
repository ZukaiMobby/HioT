from types import NoneType
from typing import Any, List, Optional

from HioT.Models.device import ModelDevice
from HioT.ModelsORM.device import (get_device_from_db_by_id,
                                   update_device_status_to_db)
from HioT.ModelsORM.user import update_user_to_db
from HioT.Plugins.get_logger import log_handler, logger
from pydantic import BaseModel
from rich import print


class ModelUser(BaseModel):
    # 用户有UserID,如果UID不存在则是为新建用户
    uid: Optional[int]
    name: str  # 用户的用户名
    password: str  # 用户密码
    privilege: int  # 用户的权限等级
    devices: Optional[List[int]]  # 列表经过转换成为字符串

    def __str__(self) -> str:
        info: str = f"用户名：{self.name};用户ID：{self.uid}"
        return info

    @log_handler
    def bind_device(self,did) -> bool:

        dev_info = get_device_from_db_by_id(did)
        dev = ModelDevice(**dev_info)
        
        if dev.bind_user != None:
            if dev.bind_user == self.uid:
                logger.info(f"用户 {self.uid} 已绑定 设备DID:{did}")
                return (False,401,f"用户 {self.uid} 已绑定 设备DID:{did}",{})
            logger.error(f"用户 {self.uid} 试图添加已被 {dev.bind_user} 添加 设备DID:{did}")
            return (False,401,f"用户 {self.uid} 试图添加已被 {dev.bind_user} 添加 设备DID:{did}",{})
        elif dev.bind_user == None:
            if type(self.devices) != NoneType:
                if did in self.devices:
                    logger.error(f"设备 {did} 没有被绑定，但是用户 {self.uid} 称其已绑定")
                    return (False,403,f"设备 {did} 没有被绑定，但是用户 {self.uid} 称其已绑定",{})

            dev.bind_user = self.uid
            if type(self.devices) == list:
                self.devices.append(did)
            elif type(self.devices) == NoneType:
                self.devices = [did]
            else:
                logger.error(f"用户 {self.uid} 绑定设备字段类型错误")
                return (False,100,f"用户 {self.uid} 绑定设备字段类型错误",{})

            print(self.dict())
            #先更新用户，不然实际上用户已经修改了，但是你如果device 更新要commit 那就格式错误了
            update_user_to_db(self.dict())  
            update_device_status_to_db(dev.dict())


            logger.info(f"用户 {self.uid} 绑定 DID:{did} 成功")
            return (True,0,f"用户 {self.uid} 绑定 DID:{did} 成功",{})
        else:
            logger.error(f"用户 {self.uid} 试图添加设备 DID:{did} 时设备绑定信息类型出错")
            return (False,100,f"用户 {self.uid} 试图添加设备 DID:{did} 时设备绑定信息类型出错",{})

    def unbind_device(self,did):

        if type(self.devices) == NoneType:
            logger.error(f"用户 {self.uid} 没有设备 {did}")
            return (False,401,f"用户 {self.uid} 没有设备 {did}",{})

        if not did in self.devices:
            logger.error(f"用户 {self.uid} 没有设备 {did}")
            return (False,401,f"用户 {self.uid} 没有设备 {did}",{})

        dev_info = get_device_from_db_by_id(did) #拿设备信息
        dev = ModelDevice(**dev_info)#生成设备实例


        if dev.bind_user != self.uid:
            logger.error(f"用户 {self.uid} 试图解绑一个不是自己的设备")
            return (False,401,f"用户 {self.uid} 试图解绑一个不是自己的设备",{})
        
        dev.bind_user = None

        try:
            self.devices.remove(did)
        except ValueError:
            logger.error(f"用户 {self.uid} 试图解绑一个不是自己的设备,但是设备称被其绑定")
            return (False,401,f"用户 {self.uid} 试图解绑一个不是自己的设备,但是设备称被其绑定",{})

        update_user_to_db(self.dict())
        update_device_status_to_db(dev.dict())
        logger.info(f"用户 {self.uid} 已解绑 设备DID:{did}")
        return (True,0,f"用户 {self.uid} 已解绑 设备DID:{did}",{})


class ModelNewUser(BaseModel):
    name: str  # 用户的用户名
    password: str  # 用户密码
    privilege: int  # 用户的权限等级

class ModeUserInfoDisplay(BaseModel):
    name: str  # 用户的用户名
    privilege: int  # 用户的权限等级
    devices: Optional[List[int]]

class ModelUpdateUser(BaseModel):
    # 用户有UserID,如果UID不存在则是为新建用户
    name: Optional[str]  # 用户的用户名
    password: Optional[str]  # 用户密码


if __name__ == '__main__':
    pass


