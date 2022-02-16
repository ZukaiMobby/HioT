from datetime import datetime
from ipaddress import AddressValueError, IPv4Address, IPv6Address
import ipaddress
import json
from types import NoneType

from typing import List, Tuple
from sqlalchemy import Column, Float, Integer, String, Boolean

from HioT.Database.sqliteDB import OrmBase, session, engine
from HioT.Plugins.get_logger import logger



class ORMDevice(OrmBase):
    # 设备实例存储位置，其中的数据应该是为当前值

    __tablename__ = 'Device'
    did = Column(Integer, primary_key=True, index=True)
    device_type_id = Column(Integer)
    bind_user = Column(Integer)
    device_name = Column(String)
    device_description = Column(String)

    online = Column(Boolean)
    keep_alive = Column(Integer)

    ipv4 = Column(Integer)
    v4port = Column(Integer)

    ipv6 = Column(Integer)
    v6port = Column(Integer)

    protocol = Column(Integer)

    last_vist = Column(Float)
    config = Column(String)  # 应为序列化之后的json
    data_item = Column(String)  # 应为序列化之后的json

    def __str__(self) -> str:
        return f"设备ID: {self.did} 设备名称: {self.device_name} 设备绑定用户: {self.bind_user} 设备描述: {self.device_description}"


OrmBase.metadata.create_all(engine)



def check_old_new_data_item(old: dict, new: dict, did: int) -> bool:

    if len(old) != len(new):
        #print(f'######old {len(old)} ######new{len(new)}')
        logger.error(f"设备ID: {did} 数据项修改出错：数据元素个数不匹配")
        return False
    try:

        for item in list(old.keys()):
            #print(f'######old {type(old[item])} ######new{type(new[item])}')
            if type(old[item]) == type(new[item]):
                pass
            else:
                logger.error(f"设备ID: {did} 数据项修改出错：数据元素类型不匹配")
                return False
        return True

    except KeyError:
        logger.error(f"设备ID: {did} 数据项修改出错：数据元素名称不匹配")
        return False



def add_device_to_db(device_model: dict ) -> Tuple[bool,int,str,dict]:
    """ 向数据库写入一个新设备 """
    from HioT.Plugins.mqtt import add_new_dev_to_subscribe
    data = {} #服务器稍后返回的数据
    if device_model['did'] != None:
        hint = f"新增设备时: 不应存在did"
        logger.error(hint)
        return (False,100,hint,{})

    else:

        if device_model['data_item'] == None or device_model['config'] == None:
            hint = f"新增设备时，数据项和配置项必须存在"
            logger.error(hint)
            return (False,100,hint,{})
        try:
            device_model['data_item'] = json.dumps(device_model['data_item'])
            device_model['config'] = json.dumps(device_model['config'])
        except json.JSONDecodeError:
            hint = f"新增设备时：数据项或配置项序列化出错"
            logger.error(hint)
            return (False,501,hint,{})
        except TypeError:
            hint = f"新增设备时: 数据项或配置项不是合法的字典类型"
            logger.error(hint)
            return (False,501,hint,{})

        the_device = ORMDevice(**device_model)

        # the_device.ipv4 = int(IPv4Address(the_device.ipv4))
        # the_device.ipv6 = int(IPv6Address(the_device.ipv6))

        if the_device.protocol == 2:
            try:
                the_device.ipv4 = int(IPv4Address(the_device.ipv4))
            except AddressValueError:
                hint = "新增设备时: IPV4解析失败"
                logger.error(hint)
                return (False,501,hint,{})
        elif the_device.protocol == 3:
            try:
                the_device.ipv6 = int(IPv6Address(the_device.ipv6))
            except AddressValueError:
                hint = "新增设备时: IPV6解析失败"
                logger.error(hint)
                return (False,501,hint,{})
        elif the_device.protocol == 1:
            try:
                the_device.ipv4 = int(IPv4Address(the_device.ipv4))
            except AddressValueError:
                hint = "新增MQTT设备时: IPV4不存在"
                logger.info(hint)

            try:
                the_device.ipv6 = int(IPv6Address(the_device.ipv6))
            except AddressValueError:
                hint = "新增MQTT设备时: IPV6不存在"
                logger.info(hint)
            
            #MQTT 在这里进行前提验证
        
        else:
            hint = "新增设备时: 用户选择了未知协议"
            logger.error(hint)
            return (False,501,hint,{})

        session.add(the_device)
        session.commit()

        if the_device.protocol == 1:
            from HioT.Plugins.get_config import mqtt_config
            data["broker"] = mqtt_config['host']
            data["bport"] = mqtt_config['port']
            data["publish_topic"] = f"did{the_device.did}publish"   #设备publish的参数【平台的subscribe】
            data["subscribe_topic"] = f"did{the_device.did}subscribe" #设备订阅参数
            data["will_message"] = f"did{the_device.did}offline"
            add_new_dev_to_subscribe(the_device.did)


        hint = f"新增设备：{str(the_device)} "
        data["did"] = the_device.did
        logger.info(hint)
        return (True,0,hint,data)


def get_device_from_db_by_id(did: int) -> dict:
    """ 根据所给的DID以字典的方式返回设备信息用于创建设备实例"""

    if type(did) != int:
        logger.error(f"获取设备 {did} 时，did非整形数值")
        return {}

    logger.debug(f"get_device_from_db_by_id的DEBUG{did}")


    device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not device:
        logger.error(f"获取设备 {did} 时，接口返回了空")
        return {}

    try:
        config = json.loads(device.config)
        data_item = json.loads(device.data_item)

    except json.JSONDecodeError:
        logger.error(f"获取设备 {did} 时，无法反序列化为字典")
        return {}
    except TypeError:
        logger.error(f"获取设备 {did} 时，数据项或配置项类型错误")
        return {}


    if device.last_vist != None:
        last_visit = datetime.fromtimestamp(device.last_vist)
    else:
        last_visit = None
    

    device_in_dict = {
        "did": device.did,
        "device_type_id": device.device_type_id,
        "bind_user": device.bind_user,
        "device_name": device.device_name,
        "device_description": device.device_description,

        "online":device.online,
        "keep_alive":device.keep_alive,
        "ipv4":device.ipv4, #######
        "ipv6":device.ipv6,
        "v4port":device.v4port,
        "v6port":device.v6port,
        "protocol":device.protocol,
        "last_vist":last_visit,
        "config": config,
        "data_item": data_item

    }


    return device_in_dict


def update_device_data_item_to_db(device_model:dict) -> Tuple[bool,int,str,dict]:
    """ 将设备更新的数据推送到INFLUX和SQLITE中 """
    try:
        did = int(device_model['did'])
        device_type_id = int(device_model['device_type_id'])

    except ValueError:

        hint = f"更新设备{did}数据项时出错：did和device_type_id应为int"
        logger.error(hint)
        return (False,403,hint,{})

    data_model = device_model['data_item']


    the_device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        hint = f"更新设备{did}数据项时出错: {did} 不存在"
        logger.error(hint)
        return (False,403,hint,{})

    try:
        old_data_model:dict = json.loads(the_device.data_item)
        new_data_model:str = json.dumps(data_model)
    except:
        hint = f"更新设备{did}数据项时出错: 数据反序列失败"
        logger.error(hint)
        return (False,403,hint,{})
    # 在这里检查数据项是否一一对应匹配
    if not check_old_new_data_item(old_data_model, data_model, did):
        return (False,403,'数据一致性检查失败，格式{"data1":value1,"data2":value2}',{})

    the_device.data_item = new_data_model
    session.commit()

    # 在这里将元素添加到influx中 #

    from HioT.Database.influxDB import influx_write

    
    line_protocol_data = str(device_type_id)+",did="+str(did)+" "

    for k, v in data_model.items():
        v = str(v)
        if len(v) == 0:
            v = '0'
        line_protocol_data += str(k)+"="+v+","

    line_protocol_data = line_protocol_data[:-1] #截掉最后一个逗号
    influx_write(line_protocol_data)

    hint = f"设备ID: {did} 数据项修改已提交"

    logger.info(hint)
    return (True,0,hint,json.loads(the_device.data_item))


def update_device_status_to_db(device_model: dict) -> Tuple[bool,int,str,dict]:
    from rich import print
    print(f"===========>BUG CHECK==={type(device_model['did'])}===")
    try:
        did = int(device_model['did'])

    except ValueError:

        hint = f"更新设备status时出错：did 不应为{type(device_model['did'])}"
        logger.error(hint)
        return (False,403,hint,{})

    device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    print(f"===========>BUG CHECK==={device.did}===")
    print(device)
    if not device:
        hint = f"更新设备status时出错: {did} 不存在"
        logger.error(hint)
        return (False,100,hint,{})

    if device_model['last_vist']: 
        time = datetime.timestamp(device_model['last_vist'])
    else:
        time = None

    device.bind_user = device_model['bind_user']
    device.device_description = device_model['device_description']
    device.device_name = device_model['device_name']
    device.online = device_model['online']
    device.protocol = device_model['protocol']
    device.v4port = device_model['v4port']
    device.v6port = device_model['v6port']
    device.keep_alive = device_model['keep_alive']
    device.last_vist = time
    
    if device.protocol == 2:
        try:
            device.ipv4 = int(IPv4Address(device_model['ipv4']))
        except ipaddress.AddressValueError:
            hint = f"更新设备status时出错: 试图使用IPV4协议，但设备IPV4地址不合法"
            logger.error(hint)
            return (False,100,hint,{})
    elif device.protocol == 3:
        try:
            device.ipv6 = int(IPv6Address(device_model['ipv6']))
        except ipaddress.AddressValueError:
            hint = f"更新设备status时出错: 试图使用IPV6协议，但设备IPV6地址不合法"
            logger.error(hint)
            return (False,100,hint,{})
    else:
        pass
    
    print("ORM层BUG检查=========>")
    print(type(device))
    print(device.bind_user)
    print(session.dirty)
    print("ORM层BUG检查=========>")
    session.commit()

    hint = f"更新设备status: {did} status已更新"
    return (True,0,hint,{})

def update_device_config_to_db(device_model: dict) -> Tuple[bool,int,str,dict]:
    config = device_model['config'] #还是一个字典需要转换成字符串
    try:
        did = int(device_model['did'])
        config = json.dumps(device_model['config'])

    except ValueError:
        hint = f"写入设备配置时出错：did或config异常"
        logger.error(hint)
        return (False,401,hint,{})

    the_device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        hint = f"写入设备配置时出错：设备 {did} 不存在"
        logger.error(hint)
        return (False,401,hint,{})

    the_device.config = config
    session.commit()

    hint = f"写入设备 {did} 配置成功"
    logger.info(hint)

    return (True,0,hint,{})


def delete_device_from_db(did: int) -> Tuple[bool,int,str,dict]:
    try:
        did = int(did)

    except ValueError:
        hint = f"删除设备时出错：did 不应为{type(did)}"
        logger.error(hint)
        return (False,403,hint,{})

    the_device: ORMDevice = session.query(ORMDevice).filter(ORMDevice.did == did).first()
    if not the_device:
        hint = f"删除设备时出错：设备{did}不存在"
        logger.error(hint)
        return (False,401,hint,{})

    session.delete(the_device)
    session.commit()

    hint = f"删除设备 {did} 成功"
    logger.info(hint)
    return (True,0,hint,{})

def get_device_not_bind_with_user():
    #返回列表【（设备ID，设备类型ID）】
    devices: List[ORMDevice] = session.query(ORMDevice).filter(ORMDevice.bind_user == None)
    return [(dev.did, dev.device_type_id) for dev in devices ]


def get_all_device_did():
    with engine.connect() as con:
        res = con.execute('SELECT did FROM Device')
        if type(res) == NoneType:
            return []
        return [ item[0] for item in res ]

if __name__ == '__main__':
    # 代码临时测试区
    pass
