from time import sleep
from types import NoneType
from HioT.Database.sqliteDB import engine
from HioT.Plugins.get_logger import logger
from HioT.Models.device import ModelDevice
from HioT.ModelsORM.device import get_device_from_db_by_id
from threading import Thread


def v46_check_online() -> None:
    while True:
        with engine.connect() as con:
            res = con.execute('SELECT did from Device where protocol == 2 or protocol == 3')
            if type(res) == NoneType:
                pass
            else:
                device_list = [ item[0] for item in res ]
                for did in device_list:
                    print(f"checker:{did}")
                    device_info:dict = get_device_from_db_by_id(did)
                    device =  ModelDevice(**device_info)
                    if device.last_vist and device.check_online():
                        logger.info(f"设备 {device.did} 状态发生变化")
        sleep(10)

online_checker = Thread(target=v46_check_online,daemon=True)