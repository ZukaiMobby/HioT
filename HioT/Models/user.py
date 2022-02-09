from typing import List, Optional, Any
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


if __name__ == '__main__':
    pass
