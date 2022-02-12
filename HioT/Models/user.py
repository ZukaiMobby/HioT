from types import NoneType
from typing import List, Optional, Tuple

from HioT.Models.device import ModelDevice
from HioT.ModelsORM.device import (get_device_from_db_by_id,
                                   update_device_status_to_db)
from HioT.ModelsORM.user import update_user_to_db
from HioT.Plugins.get_logger import logger
from pydantic import BaseModel


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

    def bind_device(self,did:int) -> Tuple[bool,int,str,dict]:
        """用户实例绑定设备的方法
        这是一个省心方法：
        调用者不需要去管数据库操作，它会"妥善"执行相关调用
        """

        
        dev_info = get_device_from_db_by_id(did)
        dev = ModelDevice(**dev_info)
        
        if dev.bind_user != None:
            if dev.bind_user == self.uid:

                hint = f"用户 {self.uid} 已绑定 设备DID:{did}"
                logger.info(hint)
                return (False,401,hint,{})
            else:

                hint = f"用户 {self.uid} 试图添加已被 {dev.bind_user} 添加 设备DID:{did}"
                logger.error(hint)
                return (False,401,hint,{})

        elif dev.bind_user == None:
            if len(self.devices) > 0:
                if did in self.devices:
                    hint = f"设备 {did} 没有被绑定，但是用户 {self.uid} 称其已绑定"
                    logger.error(hint)
                    return (False,403,hint,{})

            dev.bind_user = self.uid
            if type(self.devices) == list:
                self.devices.append(did)
            elif type(self.devices) == NoneType:
                self.devices = [did]
            else:
                hint = f"用户 {self.uid} 绑定设备字段类型错误"
                logger.error(hint)
                return (False,100,hint,{})

            #先更新用户，不然实际上用户已经修改了，但是你如果device 更新要commit 那就格式错误了
            res = update_user_to_db(self.dict())
            if not res[0]:
                return res
            res = update_device_status_to_db(dev.dict())
            if not res[0]:
                return res
            
            hint = f"用户 {self.uid} 绑定 DID:{did} 成功"
            logger.info(hint)
            return (True,0,hint,{})
        else:
            hint = f"用户 {self.uid} 绑定设备 {did} 时 dev.bind_user 类出错"
            logger.error(hint)
            return (False,100,hint,{})

    def unbind_device(self,did:int):

        if not self.devices:
            hint = f"用户 {self.uid} 没有设备"
            logger.error(hint)
            return (False,401,hint,{})

        if not did in self.devices:
            hint = f"用户 {self.uid} 没有设备 {did}"
            logger.error(hint)
            return (False,401,hint,{})

        dev_info = get_device_from_db_by_id(did) #拿设备信息

        if not dev_info:
            hint = f"获取设备 {did} 时接口返回空"
            logger.error(hint)
            return (False,401,hint,{})

        dev = ModelDevice(**dev_info)#生成设备实例


        if dev.bind_user != self.uid:
            hint = f"用户 {self.uid} 试图解绑 {dev.bind_user} 的设备"
            logger.error(hint)
            return (False,401,hint,{})
        
        dev.bind_user = None

        try:
            self.devices.remove(did)
        except ValueError:
            hint = f"用户 {self.uid} 试图解绑一个不是自己的设备,但是设备称被其绑定"
            logger.error(hint)
            return (False,401,hint,{})

        res = update_user_to_db(self.dict())

        if not res[0]:
            return res

        res = update_device_status_to_db(dev.dict())
        if not res[0]:
            return res

        hint = f"用户 {self.uid} 已解绑 设备 {did}"
        logger.info(hint)
        return (True,0,hint,{})


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
    from rich import print
    pass


