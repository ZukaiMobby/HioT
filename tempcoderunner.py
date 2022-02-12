import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse


app = FastAPI()

@app.get('/', tags=['root'])
async def app_welcome() -> str:
    """ Uvicorn 欢迎页面 """
    return "Welcome to HioT platform"


@app.get('/favicon.ico', tags=['root'])
async def favicon() -> FileResponse:
    """ 返回网站图标（就是玩.jpg） """
    return FileResponse('./HioT/imgs/favicorn.ico')


if __name__ == '__main__':

    uvicorn.run("tempcoderunner:app",log_level='info')
