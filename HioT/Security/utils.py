from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from HioT.Models.user import ModelUser
from HioT.ModelsORM.user import get_user_from_db_by_id
from HioT.Plugins.get_config import security_config
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

SECRET_KEY = security_config['syskey']
ALGORITHM = security_config['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = security_config['ACCESS_TOKEN_EXPIRE_MINUTES']

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(uid:int,pwd_to_verify:str) -> ModelUser:

    uid = int(uid)
    the_user_info = get_user_from_db_by_id(uid)

    if not the_user_info:
        return None
    
    user = ModelUser(**the_user_info)

    if not pwd_context.verify(pwd_to_verify, user.password):
        return None
    
    return user


def get_current_user_by_token(token: str = Depends(oauth2_scheme)): 
    #这应该是被depend的

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = int(payload.get("sub"))
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_info = get_user_from_db_by_id(uid)
    if user_info is None:
        raise credentials_exception
    user = ModelUser(**user_info)
    return user