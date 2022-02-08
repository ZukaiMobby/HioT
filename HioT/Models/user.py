from typing import List, Optional, Any
from pydantic import BaseModel

class ModelUser(BaseModel):
    """ 
    用例备忘：
    新建一个用户实例：
    my_user = {
    "name":"mobby",
    "password":"o345r",
    "privilege":1,
    "devices":[1201,2103,3042]
    }

    the_user = User(**my_user) 这个是一个instance

    将这个实例插入到数据库中：
    add_user_to_db(the_user.dict()) 
    这个方法在 ModelsORM.user中，新建用户时的uid必须为None

    从数据库中实例化一个用户对象：

    my_user = User(**get_user_from_db_by_id(3))
"""
    # 用户有UserID,如果UID不存在则是为新建用户
    uid: Optional[int]  
    name: str  # 用户的用户名
    password: str #用户密码
    privilege: int  # 用户的权限等级
    devices: Optional[List[int]] #列表经过转换成为字符串

    def __str__(self) -> str:
        info: str = f"用户名：{self.name};用户ID：{self.uid}"
        return info

    


if __name__ == '__main__':
    #文件测试区
    from rich import print
    from HioT.ModelsORM.user import delete_user_from_db
    delete_user_from_db(3)
    
    pass