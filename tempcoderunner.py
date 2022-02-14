from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


uvicorn.run("tempcoderunner:app")