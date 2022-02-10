from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(20),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()



if __name__ == '__main__':
    pass

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