from typing import Optional
from pydantic import BaseModel
from rich import print

from HioT.ModelsORM.device import update_device_status_to_db



class ModelDevice(BaseModel):
    """
    WARNING: 从数据库读取实例化的时候应该使用try
    错误的配置会使得接口返回空，从而导致 **失败
    """

    #这是具体的某一个设备
    did:Optional[int] #设备全局唯一的设备号
    device_type_id:int #设备所属类型
    bind_user:Optional[int] #绑定的用户UID

    device_name: Optional[str] #设备名称
    device_description: Optional[str] #设备描述
    online: Optional[bool] #设备是否在线

    config:Optional[dict] #针对某一个设备的配置，存储时应为json
    data_item: Optional[dict] #设备当前的具体数值，存储时应为json


if __name__ == '__main__':


    pass











    # #代码测试区
    # #创建一个设备[刚刚连上平台的情况]

    # the_new_dev_info = {"device_type_id":1}
    # from HioT.ModelsORM.device_type import get_device_type_from_db_by_id
    # from HioT.Models.device_type import ModelDeviceType
    # # from HioT.ModelsORM.device import add_device_to_db

    # # #获得设备的类信息
    # # typeinfo = get_device_type_from_db_by_id(the_new_dev_info['device_type_id'])
    # # #新设备信息生成
    # # gen_dev = {
    # #     "device_type_id" : the_new_dev_info['device_type_id'],
    # #     "config": typeinfo['default_config'],
    # #     "data_item": typeinfo['data_item']
    # # }
    # # #生成新设备
    # # dev = ModelDevice(**gen_dev)
    # # add_device_to_db(dev.dict())

    # from HioT.ModelsORM.device import get_device_from_db_by_id,update_device_data_item_to_db
    # dev = ModelDevice(**get_device_from_db_by_id(1))

    # dev.data_item['temp'] = 23.9
    # dev.data_item['mosi'] = 81.6
    # dev.data_item['enabled'] = True
    # dev.online = True
    # dev.bind_user = 3
    # dev.device_description = "我的设备"
    # dev.device_name = "My Power Switch"

    # print(dev.data_item)
    # update_device_data_item_to_db(data_model=dev.data_item,did=1,device_type_id=dev.device_type_id)
    # update_device_status_to_db(device_model=dev.dict(),did=dev.did)
    # # add_device_to_db(dev.dict())