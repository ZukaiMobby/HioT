from typing import Optional
from pydantic import BaseModel, PositiveInt



class ModelDeviceType(BaseModel):
    device_type_id: int
    device_type_name: str
    protocol:int

    description: Optional[str]
    keep_alive:Optional[PositiveInt]
    v4port: Optional[PositiveInt]
    v6port: Optional[PositiveInt]
    
    default_config: dict
    data_item: Optional[dict]
    

class ModelCreateDeviceType(BaseModel):
    protocol:int
    device_type_name: str
    description: Optional[str]
    keep_alive:Optional[PositiveInt]
    v4port: Optional[PositiveInt]
    v6port: Optional[PositiveInt]

    default_config: dict
    data_item: Optional[dict]
    

if __name__ == '__main__':
    from rich import print
    # 功能测试区
    pass