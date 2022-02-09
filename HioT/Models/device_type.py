"""
设备类型的Python文件
设备类型需要一个设备类型的ID
InfluxDB 的每一个measurements对应一个设备类型

这个设备类型应该是一个对象好还是每一个都是一个单独的类好呢？
{
    "device_type_id":11,
    "device_type_name":"电风扇"
    "description":"这是设备类型的描述",
    "data":{
        "湿度": 82.3,
        "温度"：23.4,
        "是否启用"： True/False,
        "开关次数": 3,
        "设备消息":"一些文本..."
        "多媒体1": "url"
        这里的data是会变化的
    }
}

"""
from typing import Optional
from pydantic import BaseModel
from rich import print


class ModelDeviceType(BaseModel):
    device_type_id: Optional[int]
    device_type_name: str
    description: Optional[str]
    data_item: Optional[dict]
    default_config: Optional[dict]  # 配置应该在新建设备类型的时候完成


if __name__ == '__main__':
    # 功能测试区

    from HioT.ModelsORM.device_type import add_device_type_to_db

    #device_type = ModelDeviceType(**get_device_type_from_db_by_id(1))
    # print(dict(device_type))

    # #指定设备id=12，比方说我这是从ORM里头拿出来的，这个字典用JSON处理一下放进去
    # a_device_type = ModelDeviceType(**the_device_type)
    # print(a_device_type.dict())

    # #我现在有个设备类型了，我想实例化一个设备应该怎么办？
    # a_device_type_info = a_device_type.dict()

    # new_device = {
    #     "device_type_id":a_device_type_info['device_type_id'],
    #     "device_name":"Home Switch",
    #     "config":a_device_type_info['default_config'],
    #     "data_item":a_device_type_info['data_item']

    # }

    # device = ModelDevice(**new_device)  #这时候完成设备的初始化

    # print(dict(device))
    # #初始化设备的时候给定一个设备类型id，我就要拿出来
