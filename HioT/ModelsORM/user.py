from types import NoneType
from typing import List, Tuple
from sqlalchemy import Column, Integer, String
from HioT.Database.sqliteDB import OrmBase,session,engine
from HioT.Plugins.get_logger import logger


class ORMUser(OrmBase):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    privilege = Column(Integer)
    devices = Column(String)

    def __str__(self) -> str:
        if self.uid == None:
            return f"用户名: {self.name}"
        else:
            return f"用户ID: {self.uid}; 用户名{self.name}"

OrmBase.metadata.create_all(engine)

def is_uid_in_db(uid:int)->bool:
    res = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not res:
        return False
    else:
        return True


def add_user_to_db(user_model: dict) -> Tuple[bool,int,str,dict]:
    """ 写入新用户 """
    if user_model['uid'] != None or user_model['devices']:
        hint = f"请求的用户{user_model['name']} 添加时存在UID或DEVICES字段"
        logger.error(hint)
        return (False,506,hint,{})
    else:
        the_user = ORMUser(**user_model)
        session.add(the_user)
        session.commit()

        hint = f"新增用户：{str(the_user)}"
        data = {"uid":the_user.uid}
        logger.info(hint)
        return (True,0,hint,data)


def get_user_from_db_by_id(uid: int) -> dict:
    """ 从数据库中取得用户信息，错误返回空 """
    """ 从这里拿出来的数据就不要动，动了就提交！！不然BUG要无限多了 """
    if type(uid) != int:
        logger.error(f"查询的用户UID不是int， 是{type(uid)}")
        return {}
        

    user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == int(uid)).first()
    if type(user) == NoneType:
        return {}

    if type(user.devices) == str:

        devices_in_str = user.devices.split()
        devices_in_str = list(map(int,devices_in_str))
        
    elif type(user.devices) == NoneType:
        devices_in_str = None

    else:
        logger.error(f"取得用户{uid}信息时，其设备列表不为字符串或空为{type(user.devices)}")
        return {}

    user_in_dict = {
        "uid":uid,
        "name":user.name,
        "password":user.password,
        "privilege":user.privilege,
        "devices":devices_in_str
    }
    return user_in_dict

def get_all_user_uid_from_db() -> List[int]:
    
    with engine.connect() as con:
        result_raw = con.execute('SELECT uid FROM users')
        result_raw = list(result_raw)
        return [ item[0] for item in result_raw ]


def update_user_to_db(user_model: dict):
    """ 更新用户数据到数据库 """
    if user_model['uid'] == None:
        hint = f"写入用户信息是UID字段不存在"
        logger.error(hint)
        return (False,402,hint,{})
    else:
        user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == int(user_model['uid'])).first()

        if user == None:
            hint = f"请求更新的用户不在数据库中"
            logger.error(hint)
            return (False,402,hint,{})

        user.name = user_model['name']
        user.password = user_model['password']
        user.privilege = user_model['privilege']
        #记得将数组转换为字符串
        if type(user_model['devices']) == list:
            user_model['devices'] = " ".join(map(str,user_model['devices']))
            user.devices = user_model['devices']
        elif type(user_model['devices']) == NoneType:
            user.devices = None
        else:
            hint = f"请求更新的用户 {user.uid} 设备列表为{type(user.devices)},应为list或None"
            logger.error(hint)
            return (False,402,hint,{})

        session.commit() #提交修改
        hint = f"更新用户 {user.uid} 成功"
        logger.info(hint)
        return (True,0,hint,{})

def delete_user_from_db(uid: int) -> Tuple[bool,int,str,dict]:
    user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not user:
        hint = f"请求删除的用户：{uid} 不存在"
        logger.error(hint)
        return (False,402,hint,{})
    else:
        session.delete(user)
        session.commit()
        logger.info(f"请求删除的用户：{uid} 成功")
        return (True,0,f"请求删除的用户：{uid} 成功",{})



if __name__ == '__main__':
    #文件测试区
    pass