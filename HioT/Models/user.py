from types import NoneType
from typing import List, Optional, Any
from pydantic import BaseModel
from HioT.Models.device import ModelDevice
from HioT.ModelsORM.device import get_device_from_db_by_id,ORMDevice, get_device_not_bind_with_user,update_device_status_to_db
from HioT.ModelsORM.user import update_user_to_db,get_user_from_db_by_id
from HioT.Plugins.get_logger import log_handler,logger
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
                return False
            logger.error(f"用户 {self.uid} 试图添加已被 {dev.bind_user} 添加 设备DID:{did}")
            return False
        elif dev.bind_user == None:
            if did in self.devices:
                logger.error(f"设备 {did} 没有被绑定，但是用户 {self.uid} 称其已绑定")
                return False

            dev.bind_user = self.uid
            if type(self.devices) == list:
                self.devices.append(did)
            elif type(self.devices) == NoneType:
                self.devices = [did]
            else:
                logger.error(f"用户 {self.uid} 绑定设备字段类型错误")

            print(self.dict())
            #先更新用户，不然实际上用户已经修改了，但是你如果device 更新要commit 那就格式错误了
            update_user_to_db(self.dict())  
            update_device_status_to_db(dev.dict())


            logger.info(f"用户 {self.uid} 绑定 DID:{did} 成功")
            return True
        else:
            logger.error(f"用户 {self.uid} 试图添加设备 DID:{did} 时设备绑定信息类型出错")
            return False

    def unbind_device(self,did):
        if not did in self.devices:
            logger.error(f"用户 {self.uid} 没有设备 {did}")
            return False

        dev_info = get_device_from_db_by_id(did) #拿设备信息
        dev = ModelDevice(**dev_info)#生成设备实例


        if dev.bind_user != self.uid:
            logger.error(f"用户 {self.uid} 试图解绑一个不是自己的设备")
            return False
        
        dev.bind_user = None

        try:
            self.devices.remove(did)
        except ValueError:
            logger.error(f"用户 {self.uid} 试图解绑一个不是自己的设备,但是设备称被其绑定")
            return False

        update_user_to_db(self.dict())
        update_device_status_to_db(dev.dict())
        logger.info(f"用户 {self.uid} 已解绑 设备DID:{did}")
        return True

if __name__ == '__main__':
    user = ModelUser(**get_user_from_db_by_id(1))
    # user.unbind_device(1)
    # user.bind_device(1)
    # user.bind_device(1)
    # user.bind_device(4)
    # user.bind_device(3)
    # user.unbind_device(3)
    # print(get_device_not_bind_with_user())
    


