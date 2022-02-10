""" 将dev模型实际的存入到数据库中 """
import json
from types import NoneType

from typing import List, Tuple
from sqlalchemy import Column, Integer, String, Boolean

from HioT.Database.sqliteDB import OrmBase, session, engine
from HioT.Plugins.get_logger import log_handler, logger

class ORMDevice(OrmBase):
    # 设备实例存储位置，其中的数据应该是为当前值

    __tablename__ = 'Device'
    did = Column(Integer, primary_key=True, index=True)
    device_type_id = Column(Integer)
    bind_user = Column(Integer)

    device_name = Column(String)
    device_description = Column(String)
    online = Column(Boolean)

    config = Column(String)  # 应为序列化之后的json
    data_item = Column(String)  # 应为序列化之后的json

    def __str__(self) -> str:
        return f"设备ID: {self.did} 设备名称: {self.device_name} 设备绑定用户: {self.bind_user} 设备描述: {self.device_description}"


OrmBase.metadata.create_all(engine)


###############验证类函数开始################

def check_old_new_data_item(old: dict, new: dict, did: int) -> bool:
    # print(old)
    # print(new)
    if len(old) != len(new):
        logger.error(f"设备ID: {did} 数据项修改出错：数据元素个数不匹配")
        return False
    try:
        for item in list(old.keys()):
            if type(old[item]) == type(new[item]):
                pass
            else:
                logger.error(f"设备ID: {did} 数据项修改出错：数据元素类型不匹配")
                return False
    except KeyError:
        logger.error(f"设备ID: {did} 数据项修改出错：数据元素名称不匹配")
        return False
    return True

###############验证类函数结束################

@log_handler
def add_device_to_db(device_model: dict) -> bool:

    if device_model['did'] == None:
        # 新建一个设备至数据库
        if type(device_model['data_item']) == None:
            logger.error(f"写入设备数据时出错：必须存在至少一个数据项")
            return False
        if type(device_model['data_item']) == dict:
            device_model['data_item'] = json.dumps(device_model['data_item'])
        else:
            logger.error(f"写入设备数据时出错：数据项必须是字典类型")

        if type(device_model['config']) == dict:
            device_model['config'] = json.dumps(device_model['config'])

        if not type(device_model['data_item']) == str:
            logger.error(
                f"写入设备数据时出错：无法从 {type(device_model['data_item'])} 转换为 str")
            return False
        if type(device_model['config']) != NoneType:
            if type(device_model['config']) != str:
                logger.error(
                    f"写入设备数据时出错：无法从 {type(device_model['config'])} 转换为 str")

        the_device = ORMDevice(**device_model)
        session.add(the_device)
        session.commit()
        logger.info("新增设备： "+str(the_device))
        return True
    else:
        logger.error(f"请求添加的设备{device_model['device_name']} 添加时存在did字段")
        return False


@log_handler
def get_device_from_db_by_id(did: int) -> dict:
    # 从数据库中查询（获取）一个设备

    if not type(did) == int:
        logger.error(f"设备DID应为int, 不是{type(did)}")
        return {}
    the_device: ORMDevice = session.query(
        ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        logger.error(f"设备DID:{did} 不存在")
        return {}
    config = None
    if type(the_device.config) == str:
        config = json.loads(the_device.config)
    elif type(the_device.config) == NoneType:
        pass
    else:
        logger.error(f"读取设备信息时发生转换错误:{type(the_device.config)}应为str或None")

    the_device_in_dict = {
        "did": the_device.did,
        "device_type_id": the_device.device_type_id,
        "bind_user": the_device.bind_user,
        "device_name": the_device.device_name,
        "device_description": the_device.device_description,
        "config": config,
        "data_item": json.loads(the_device.data_item),
    }
    return the_device_in_dict


@log_handler
def update_device_data_item_to_db(device_model:dict) -> bool:
    # 设备更新数据时注意要将数据同步到Influx中
    # 对于一些数据需要回传给设备已及时更新状态
    # 写入之前需要检查一下新来的字段是否完整，是否多了少了，不然写到数据库中后果严重

    did = device_model['did']
    data_model = device_model['data_item']
    device_type_id = device_model['device_type_id']

    if not type(did) == int:
        logger.error(f"设备DID应为int, 不是{type(did)}")
        return False
    the_device: ORMDevice = session.query(
        ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        logger.error(f"设备DID: {did} 不存在")
        return False

    # 在这里检查数据项是否一一对应匹配
    if not check_old_new_data_item(json.loads(the_device.data_item), data_model, did):
        return False

    the_device.data_item = json.dumps(data_model)
    session.commit()

    # 在这里将元素添加到influx中

    from HioT.Database.influxDB import influx_write

    #data = "mem,host=host1 used_percent=23.43234543"
    # <measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
    line_protocol_data = str(device_type_id)+",did="+str(did)+" "

    for k, v in data_model.items():
        v = str(v)
        if len(v) == 0:
            v = '0'
        line_protocol_data += str(k)+"="+v+","
    line_protocol_data = line_protocol_data[:-1]
    print(line_protocol_data)

    influx_write(line_protocol_data)

    logger.info(f"设备ID: {did} 数据项修改已提交")


@log_handler
def update_device_status_to_db(device_model: dict,immediate_commit = True ) -> bool:

    did = device_model['did']
    if not type(did) == int:
        logger.error(f"设备DID应为int, 不是{type(did)}")
        return False
    the_device: ORMDevice = session.query(
        ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        logger.error(f"设备DID: {did} 不存在")
        return False

    if the_device.device_type_id != device_model['device_type_id']:
        logger.error(f"设备DID: {did} 不得修改设备类型")
        return False

    the_device.bind_user = device_model['bind_user'] #这里需要把列表重新序列化
    the_device.device_description = device_model['device_description']
    the_device.device_name = device_model['device_name']
    the_device.online = device_model['online']
    
    if immediate_commit:
        session.commit()
        logger.info(f"设备DID: {did} 状态已更新")
    else:
        logger.info(f"设备DID: {did} 状态更新已缓存")
    return True


@log_handler
def update_device_config_to_db(device_model: dict) -> bool:
    config = device_model['config'] #还是一个字典需要转换成字符串
    did = device_model['did']

    if not type(did) == int:
        logger.error(f"设备DID应为int, 不是{type(did)}")
        return False
    the_device: ORMDevice = session.query(
        ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        logger.error(f"设备DID: {did} 不存在")
        return False

    the_device.config = json.dumps(config)
    logger.info(f"设备DID: {did} 配置更新成功")
    return True


@log_handler
def device_config_push_to_device():
    pass


@log_handler
def delete_device_from_db(did: int) -> bool:
    #删除设备，也要删除历史数据

    the_device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        #所删除的设备不存在
        logger.error(f"请求删除的设备：{did} 不存在")
        return False
    session.delete(the_device)
    session.commit()
    the_device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        logger.info(f"请求删除的设备：{did} 成功")
        return True
    else:
        logger.error(f"请求删除的设备：{did} 失败，请检查")
        return False

@log_handler

def get_device_not_bind_with_user():
    #返回列表【（设备ID，设备类型ID）】
    the_devices: List[ORMDevice] = session.query(ORMDevice).filter(ORMDevice.bind_user == None)
    res = []
    for device in the_devices:
        res.append((device.did,device.device_type_id))
    return res

if __name__ == '__main__':
    # 代码临时测试区
    print(get_device_not_bind_with_user())
    pass
