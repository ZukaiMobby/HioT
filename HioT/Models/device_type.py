from typing import Optional
from pydantic import BaseModel, PositiveInt



class ModelDeviceType(BaseModel):
    device_type_id: Optional[int]
    device_type_name: str
    description: Optional[str]

    keep_alive:Optional[int]
    v4port: Optional[PositiveInt]
    v6port: Optional[PositiveInt]
    protocol:Optional[int]

    data_item: Optional[dict]
    default_config: Optional[dict]

class ModelCreateDeviceType(BaseModel):
    device_type_name: str
    description: Optional[str]
    data_item: Optional[dict]
    default_config: Optional[dict]
    keep_alive:Optional[int]
    v4port: Optional[PositiveInt]
    v6port: Optional[PositiveInt]
    protocol:Optional[int]

if __name__ == '__main__':
    from rich import print
    # 功能测试区
    pass