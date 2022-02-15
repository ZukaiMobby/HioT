import json
from types import NoneType
from rich import print
from typing import List, Tuple
from sqlalchemy import Column, Integer, String

from HioT.Database.sqliteDB import OrmBase, session, engine
from HioT.Models.device import ModelDevice
from HioT.Models.user import ModelUser
from HioT.ModelsORM.device import delete_device_from_db, get_device_from_db_by_id
from HioT.ModelsORM.user import get_user_from_db_by_id
from HioT.Plugins.get_logger import logger

p_mqtt = 1
p_ipv4 = 2
p_ipv6 = 3


class ORMDeviceType(OrmBase):
    __tablename__ = 'DeviceType'
    device_type_id = Column(Integer, primary_key=True, index=True)
    device_type_name = Column(String)
    description = Column(String)

    keep_alive = Column(Integer)
    v4port = Column(Integer)
    v6port = Column(Integer)
    protocol = Column(Integer)

    data_item = Column(String)  # 应该是Json序列化后的结果
    default_config = Column(String)  # 应该是Json序列化后的结果

    def __str__(self) -> str:
        return f"设备类型ID: {self.device_type_id}; \
        名称：{self.device_type_name}; \
        描述：{self.description}"

OrmBase.metadata.create_all(engine)


def add_device_type_to_db(type_info: dict) -> Tuple[bool,int,str,dict]:
    """ 从ModelDeviceType中抽取并插入数据库 """

    if type_info['device_type_id'] == None:
        #新建一个设备类型

        if not type_info['keep_alive']:
            hint = f"新增设备类型出错：必须设置 keep_alive"
            logger.error(hint)
            return (False,332,hint,{})
        else:
            type_info['keep_alive'] = int(type_info['keep_alive'])
        
        if not type_info['protocol']:
            hint = f"新增设备类型出错：必须设置 protocol"
            logger.error(hint)
            return (False,332,hint,{})
        else:
            type_info['protocol'] = int(type_info['protocol'])

            if type_info['protocol'] == p_ipv4:

                if not type_info['v4port']:
                    print(f"========>{type_info['v4port']}")
                    hint = f"新增设备类型出错：ipv4 必须设置 v4port"
                    logger.error(hint)
                    return (False,332,hint,{})
                elif int(type_info['v4port']) <= 0:
                    hint = f"新增设备类型出错：vport4 需大于0"
                    logger.error(hint)
                    return (False,332,hint,{})
                else:
                    pass
            elif type_info['protocol'] == p_ipv6:
                if not type_info['v6port']:
                    hint = f"新增设备类型出错：ipv6 必须设置 vport6"
                    logger.error(hint)
                    return (False,332,hint,{})
                elif int(type_info['v6port']) <= 0:
                    hint = f"新增设备类型出错：vport6 需大于0"
                    logger.error(hint)
                    return (False,332,hint,{})
                else:
                    pass
            elif type_info['protocol'] == p_mqtt:
                #后续如果需要MQTT相关认证加这里
                pass
            else:
                hint = f"新增设备类型出错：不支持的协议类型"

        if not type_info['data_item']:
            hint = f"新增设备类型出错：必须存在至少一个数据项"
            logger.error(hint)
            return (False,332,hint,{})

        elif type(type_info['data_item']) == dict:
            type_info['data_item'] = json.dumps(type_info['data_item'])
        else:
            hint = f"新增设备类型出错：数据项必须是字典类型"
            logger.error(hint)
            return (False,332,hint,{})

        if type_info['default_config'] and type(type_info['default_config']) == dict:
            type_info['default_config'] = json.dumps(type_info['default_config'])
        else:
            hint = f"新增设备类型出错：default_config 为{type(type_info['default_config'])}"
            logger.error(hint)
            return (False,332,hint,{})

        device_type_in_dict = {
            "device_type_name": type_info['device_type_name'],
            "description":type_info['description'],
            "data_item":type_info['data_item'],
            "default_config":type_info['default_config'],
            "keep_alive":type_info['keep_alive'],
            "v4port":type_info['v4port'],
            "v6port":type_info['v6port'],
            "protocol":type_info['protocol']
        }
        

        the_device_type = ORMDeviceType(**device_type_in_dict)
        session.add(the_device_type)
        session.commit()

        hint = f"新增设备类型:{str(the_device_type)}"
        data = {"device_type_id":the_device_type.device_type_id}

        logger.info(hint)
        return (True,0,hint,data)

    else:
        hint = f"请求的用户{type_info['device_type_name']} 添加时存在device_type_id字段"
        logger.error(hint)
        return (False,332,hint,{})



def get_device_type_from_db_by_id(device_type_id: int) -> dict:
    if type(device_type_id) != int:
        logger.error(f"请求获得的设备类型时应是int，而非{type(device_type_id)}")
        return {}

    the_device_type: ORMDeviceType = session.query(ORMDeviceType).\
        filter(ORMDeviceType.device_type_id == device_type_id).first()

    if not the_device_type:
        logger.error(f"请求获得的设备类型{device_type_id} 不存在")
        return {}

    try:
        data_item = json.loads(the_device_type.data_item)
        default_config = json.loads(the_device_type.default_config)
    except json.JSONDecodeError:
        logger.error(f"DB中设备类型Json格式转换错误")
        return {}
    except TypeError:
        logger.error(f"DB中设备类型不支持JSON转换的格式")
        return {}

    the_device_type_in_dict = {
        "device_type_id":the_device_type.device_type_id,
        "device_type_name":the_device_type.device_type_name,
        "description":the_device_type.description,
        "keep_alive":the_device_type.keep_alive,
        "v4port":the_device_type.v4port,
        "v6port":the_device_type.v6port,
        "protocol":the_device_type.protocol,

        "data_item":data_item,
        "default_config":default_config

    }

    hint = f"设备类型获取成功:{the_device_type.device_type_id}"
    logger.info(hint)
    return the_device_type_in_dict


def get_all_device_type_from_db():
    with engine.connect() as con:
        result_raw = con.execute('SELECT device_type_id FROM DeviceType')
        if not result_raw:
            return []
        return [ tid[0] for tid in result_raw]


def delete_device_type_from_db(device_type_id: int) -> Tuple[bool,int,str,dict]:
    logger.warning("删除设备类型将同时删除该类型的设备及其连接!")

    if type(device_type_id) != int:

        hint = f"请求获得的设备类型时应是int，而非{type(device_type_id)}"
        logger.error(hint)
        return (False,541,hint,{})

    the_device_type: ORMDeviceType = session.query(ORMDeviceType).filter(ORMDeviceType.device_type_id == device_type_id).first()

    if not the_device_type:
        hint = f"请求获得的设备类型{device_type_id} 不存在"
        logger.error(hint)
        return (False,541,hint,{})

    session.delete(the_device_type)
    session.commit()

    the_device_type: ORMDeviceType = session.query(ORMDeviceType).\
        filter(ORMDeviceType.device_type_id == device_type_id).first()
    
    if not the_device_type:

        logger.info(f"请求删除的设备类型 {device_type_id} 成功")

        with engine.connect() as con:
            result_raw = con.execute(f'SELECT did from Device where device_type_id == {device_type_id}')
            result_raw = list(result_raw)

            did_list = [ item[0] for item in result_raw]

            if did_list: #设备类型绑定了设备
                for did in did_list:

                    logger.info(f"正在删除设备 {did} 并解绑用户 ")
                    the_device_info = get_device_from_db_by_id(did)

                    if the_device_info:  #设备信息查询成功
                        the_device = ModelDevice(**the_device_info)

                        if the_device.bind_user != None:
                            user_info = get_user_from_db_by_id(the_device.bind_user)

                            if user_info:

                                the_user = ModelUser(**user_info)
                                the_user.unbind_device(did)
                            else:
                                logger.info(f"设备绑定了一个不存在的用户 {the_device.bind_user} ")
                        else:
                            logger.info(f"设备{the_device.did}没有绑定用户")

                        delete_device_from_db(did)
                    else:
                        hint = f"请求删除的设备 {did} 查询为空"
                        logger.error(hint)
                        return (False,541,hint,{})

            else:
                logger.info(f"设备类型 {device_type_id} 没有绑定设备")

        hint = f"请求删除的设备类型{device_type_id} 成功"
        logger.info(hint)
        return (True,0,hint,{})

    else:
        hint = f"请求删除的设备类型{device_type_id} 失败"
        logger.error(hint)
        return (False,541,hint,{})

if __name__ == '__main__':
    pass

