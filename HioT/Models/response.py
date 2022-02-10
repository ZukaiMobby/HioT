from typing import Any, Optional
from pydantic import BaseModel


class CommonResponseModel(BaseModel):
    errno:int = 0
    message: Optional[str]
    data:Any