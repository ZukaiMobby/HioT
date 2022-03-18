import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from HioT.Plugins.get_logger import logger
from HioT.Plugins.check_env import check_for_initialize
from HioT.Plugins.get_config import *
from HioT.Plugins.scheduler import online_checker
from HioT.Plugins.mqtt import client
from HioT.Routers import device as route_device
from HioT.Routers import sdk as route_sdk
from HioT.Routers import setting as route_setting
from HioT.Routers import user as route_user


app = FastAPI()
@app.on_event("startup")
async def startup():
    check_for_initialize()
    online_checker.start()

@app.on_event("shutdown")
def shutdown():
    client.loop_stop()



@app.get('/', tags=['root'])
async def app_welcome() -> str:
    """ Uvicorn 欢迎页面 """
    return FileResponse('./panel/index.html')


@app.get('/favicon.ico', tags=['root'])
async def favicon() -> FileResponse:
    """ 返回网站图标（就是玩.jpg） """
    return FileResponse('./HioT/images/favicorn.ico')

app.include_router(route_device.router)
app.include_router(route_user.router)
app.include_router(route_sdk.router)
app.include_router(route_setting.router)
app.mount("/panel", StaticFiles(directory="panel"), name="panel")


if __name__ == '__main__':
    check_for_initialize()
    uvicorn.run("main:app", log_level='error',
                host=uvicorn_config['host'], port=uvicorn_config['port'])
