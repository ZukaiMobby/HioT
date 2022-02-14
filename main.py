import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

from HioT.Plugins.check_env import check_for_initialize
from HioT.Plugins.get_config import *
from HioT.Plugins.scheduler import scheduler
import HioT.Plugins.mqtt 
from HioT.Routers import device as route_device
from HioT.Routers import sdk as route_sdk
from HioT.Routers import setting as route_setting
from HioT.Routers import user as route_user


app = FastAPI()
info = '''
Welcome to HioT platform

Here are some notes
1. Do not run behind a proxy
'''

@app.get('/', tags=['root'])
async def app_welcome() -> str:
    """ Uvicorn 欢迎页面 """
    return info


@app.get('/favicon.ico', tags=['root'])
async def favicon() -> FileResponse:
    """ 返回网站图标（就是玩.jpg） """
    return FileResponse('./HioT/imgs/favicorn.ico')

app.include_router(route_device.router)
app.include_router(route_user.router)
app.include_router(route_sdk.router)
app.include_router(route_setting.router)


if __name__ == '__main__':
    check_for_initialize()
    uvicorn.run("main:app", log_level='info',
                host=uvicorn_config['host'], port=uvicorn_config['port'])
