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
    pass