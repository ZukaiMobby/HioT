from types import NoneType
from typing import List
from sqlalchemy import Column, Integer, String

from HioT.Database.sqliteDB import OrmBase,session,engine
from HioT.Plugins.get_logger import log_handler, logger


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



def is_uid_in_db(uid:int)->bool:
    res = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not res:
        return False
    else:
        return True

@log_handler
def add_user_to_db(user_model: dict) -> bool:
    """ 从User模型中抽取设备列表并转换到字符串并插入数据库 """
    if user_model['uid'] == None:
        #新建一个用户
        if user_model['devices']:
            user_model['devices'] = " ".join(map(str,user_model['devices']))
        the_user = ORMUser(**user_model)
        logger.debug("添加前： "+str(the_user))
        session.add(the_user)
        session.commit()
        logger.info("新增用户： "+str(the_user))
        return True
    else:
        logger.error(f"请求的用户{user_model['name']} 添加时存在UID字段")
        return False
    

@log_handler
def get_user_from_db_by_id(uid: int) -> dict:
    # 当查询的用户不存在时会返回空字典
    the_user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not the_user:
        return {}
    the_user.devices = the_user.devices.split()
    the_user.devices = list(map(int,the_user.devices))
    the_user_in_dict = {
        "uid":the_user.uid,
        "name":the_user.name,
        "password":the_user.password,
        "privilege":the_user.privilege,
        "devices":the_user.devices
    }
    return the_user_in_dict


@log_handler
def update_user_to_db(user_model) -> bool:
    if user_model['uid'] == None:
        logger.error(f"请求的用户{user_model['name']} 更新时UID字段不存在")
    else:
        the_user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == user_model['uid']).first()

        if the_user == None:
            logger.error(f"请求的UID{user_model['uid']} 不在数据库中")
            return False

        the_user.name = user_model['name']
        the_user.password = user_model['password']
        the_user.privilege = user_model['privilege']
        #记得将数组转换为字符串
        if type(user_model['devices']) == list:
            logger.debug(f"更新用户{user_model['name']} ,正在转换字符串")
            user_model['devices'] = " ".join(map(str,user_model['devices']))
        the_user.devices = user_model['devices']

        session.commit() #提交修改
        return True
        
    


@log_handler
def delete_user_from_db(uid: int) -> bool:
    the_user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not the_user:
        #所删除的用户不存在
        logger.error(f"请求删除的用户：{uid} 不存在")
        return False
    session.delete(the_user)
    session.commit()
    the_user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == uid).first()
    if not the_user:
        logger.info(f"请求删除的用户：{uid} 成功")
        return True
    else:
        logger.error(f"请求删除的用户：{uid} 失败，请检查")
        return False


OrmBase.metadata.create_all(engine)
if __name__ == '__main__':
    #文件测试区
    pass