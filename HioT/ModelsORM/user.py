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
def add_user_to_db(user_model):
    """ 从User模型中抽取设备列表并转换到字符串并插入数据库 """
    if user_model['uid'] == None:
        #新建一个用户
        
        user_model['devices'] = " ".join(map(str,user_model['devices']))
        the_user = ORMUser(**user_model)
        logger.debug("添加前： "+str(the_user))
        session.add(the_user)
        session.commit()
        logger.info("新增用户： "+str(the_user))
    

@log_handler
def get_user_from_db_by_id(uid: int) -> dict:
    print("-----")
    the_user: ORMUser = session.query(ORMUser).filter(ORMUser.uid == uid).first()
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
def update_user_to_db(user_model):
    pass


@log_handler
def delete_user_from_db(user_model):
    pass
        


OrmBase.metadata.create_all(engine)
if __name__ == '__main__':
    #文件测试区
    pass