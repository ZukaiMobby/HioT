import json
from types import NoneType

from typing import List
from sqlalchemy import Column, Integer, String

from HioT.Database.sqliteDB import OrmBase, session, engine
from HioT.Plugins.get_logger import log_handler, logger

# class ModelDeviceType(BaseModel):
#     device_type_id: Optional[int]
#     device_type_name: str
#     description: Optional[str]
#     data_item: Optional[dict] #in json
#     default_config: Optional[str] #配置应该在新建设备类型的时候完成


class ORMDeviceType(OrmBase):
    __tablename__ = 'DeviceType'
    device_type_id = Column(Integer, primary_key=True, index=True)
    device_type_name = Column(String)
    description = Column(String)

    data_item = Column(String)  # 应该是Json序列化后的结果
    default_config = Column(String)  # 应该是Json序列化后的结果

    def __str__(self) -> str:
        return f"设备类型ID: {self.device_type_id}; \
        名称：{self.device_type_name}; \
        描述：{self.description}"

OrmBase.metadata.create_all(engine)

@log_handler
def add_device_type_to_db(device_type_model: dict) -> bool:
    """ 从ModelDeviceType中抽取并插入数据库 """
    if device_type_model['device_type_id'] == None:
        #新建一个设备类型

        if type(device_type_model['data_item']) == None:
            logger.error(f"保存设备类型时出错：必须存在至少一个数据项")
            return False
        if type(device_type_model['data_item']) == dict:
            device_type_model['data_item'] = json.dumps(device_type_model['data_item'])
        else:
            logger.error(f"保存设备类型时出错：数据项必须是字典类型")

        if type(device_type_model['default_config']) == dict:
            device_type_model['default_config'] = json.dumps(device_type_model['default_config'])

        if not type(device_type_model['data_item']) == str:
            logger.error(f"保存设备类型时出错：无法从 {type(device_type_model['data_item'])} 转换为 str")
            return False
        if type(device_type_model['default_config']) != NoneType:
            if type(device_type_model['default_config']) != str:
                logger.error(f"保存设备类型时出错：无法从 {type(device_type_model['default_config'])} 转换为 str")

        device_type_in_dict = {
        "device_type_name": device_type_model['device_type_name'],
        "description":device_type_model['description'],
        "data_item":device_type_model['data_item'],
        "default_config":device_type_model['default_config']}
        the_device_type = ORMDeviceType(**device_type_in_dict)
        session.add(the_device_type)
        session.commit()
        logger.info("新增设备类型： "+str(the_device_type))

    else:
        logger.error(f"请求的用户{device_type_model['device_type_name']} 添加时存在device_type_name字段")
        return False


@log_handler
def get_device_type_from_db_by_id(device_type_id: int) -> dict:
    if type(device_type_id) != int:
        logger.error(f"请求获得的设备类型时应是int，而非{type(device_type_id)}")
        return {}
    the_device_type: ORMDeviceType = session.query(ORMDeviceType).\
        filter(ORMDeviceType.device_type_id == device_type_id).first()

    if not the_device_type:
        logger.error(f"请求获得的设备类型{device_type_id} 不存在")
        return {}
    the_default_config = None
    if type(the_device_type.default_config) == NoneType:
        pass
    elif type(the_device_type.default_config) == str:
        the_default_config = json.loads(the_device_type.default_config)
    else:
        logger.error(f"设备类型默认配置转换出错：{type(the_device_type.default_config)},应为str或者None")

    the_device_type_in_dict = {
    "device_type_id":the_device_type.device_type_id,
    "device_type_name":the_device_type.device_type_name,
    "description":the_device_type.description,
    "data_item":json.loads(the_device_type.data_item),
    "default_config":the_default_config}
    logger.info(f"设备类型获取成功:{the_device_type.device_type_id}")
    return the_device_type_in_dict


@log_handler
def update_device_type_to_db(user_model) -> bool:
    logger.error("设备类型不能被更新，请删除类型并重建")
    return False
        
    


@log_handler
def delete_device_type_from_db(uid: int) -> bool:
    logger.warning("删除设备类型将导致所有该类型设备的历史数据丢失、所有设备需要重新配置并连接..")
    pass