from datetime import datetime, timedelta
from types import NoneType
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

#=====api权限常量=====#

ROOT                    = 00    #管理员权限，无视其它规则
LOGIN_SELF_AND_DEVICE   = 10    #需要验证自己是自己，设备是自己的
LOGIN_SELF              = 20    #仅需要验证自己是自己
LOGIN                   = 30    #仅需要登入即可（比如在绑定设备时）
ANONYMOUS               = 50    #不需要任何验证

#=====用户权限常量=====#
#定义在user.privilige中
#   root 用户置为 0
#非 root 置为     1

#======权限不足错误=======

privilige_exception = HTTPException(
        status_code=401,
        detail="Permission Denied",
        headers={"WWW-Authenticate": "Bearer"},
    )

type_exception = HTTPException(
        status_code=422,
        detail="Error field data type received",
    )

def gen_operation_privilige(user: ModelUser = None, target_uid:int = None, target_did:int = None) -> int:
    #用于生成本次操作的权限等级


    if type(user) == NoneType:
        return ANONYMOUS

    elif user.privilege == 0: #登入了root用户
        return ROOT

    elif user.privilege == 1: #常规用户
        if user.uid == target_uid:
            
            if user.devices and target_did in user.devices:
                return LOGIN_SELF_AND_DEVICE
            else:
                return LOGIN_SELF
        else:
            return LOGIN
    else:
        return ANONYMOUS #不知名的用户
    

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(uid:int,pwd_to_verify:str) -> dict:
    """ 验证成功之后返回的用户字典 """
    try:
        assert type(uid) == int
        assert type(pwd_to_verify) == str
    except AssertionError:
        raise type_exception
    
    usr_info = get_user_from_db_by_id(uid)

    if not usr_info and not pwd_context.verify(pwd_to_verify, usr_info['password']):
        return {}
        
    return usr_info


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