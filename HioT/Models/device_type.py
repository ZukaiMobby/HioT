from typing import Optional
from pydantic import BaseModel



class ModelDeviceType(BaseModel):
    device_type_id: Optional[int]
    device_type_name: str
    description: Optional[str]
    data_item: Optional[dict]
    default_config: Optional[dict]

class ModelCreateDeviceType(BaseModel):
    device_type_name: str
    description: Optional[str]
    data_item: Optional[dict]
    default_config: Optional[dict]

if __name__ == '__main__':
    from rich import print
    # 功能测试区
    pass