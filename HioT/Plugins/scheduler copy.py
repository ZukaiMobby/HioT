from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from HioT.Plugins.get_config import scheduler_config

jobstores = {'default': MemoryJobStore()}
executors = {'default': ThreadPoolExecutor(20),}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')
scheduler.start()

def v46_check_online():
    from HioT.Models.device import ModelDevice
    from HioT.ModelsORM.device import get_all_device_did, get_device_from_db_by_id
    from HioT.Plugins.get_logger import logger

    device_list = get_all_device_did()
    for did in device_list:
        dev:dict = get_device_from_db_by_id(did)
        if not dev:
            continue
        else:
            if dev['protocol'] == 2 or dev['protocol'] == 3:
                device =  ModelDevice(**dev)
                
                if device.last_vist and device.check_online():
                    logger.info(f"设备 {device.did} 状态发生变化")

scheduler.add_job(func=v46_check_online, trigger='interval', seconds=scheduler_config['interval'])


















#使用装饰器的方式进行调度
#scheduler.add_job(id=job_id, func=job, args=(job_id,), trigger='interval', seconds=2)
# @scheduler.scheduled_job(trigger='interval', seconds=3,args=(4,))
# def job(num):
#     print(f"....{num}.....")

# for i in range(10):
#     sleep(3)

# @app.post('/remove-job')
# async def remove_job(job_id: str = Body(..., embed=True)):
# """移除job"""
# scheduler.remove_job(job_id)
# return {"msg": "success!"}