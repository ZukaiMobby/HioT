from fastapi import APIRouter
from HioT.Repository import sdk

router = APIRouter(
    tags=["sdk"],
    prefix="/sdk"
)


@router.get('/sdk')
def get_sdk_list():
    """ 获得所有在册SDK列表 """
    return sdk.get_sdk_list()

