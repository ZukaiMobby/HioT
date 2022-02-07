from fastapi import APIRouter
from HioT.Repository import user

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.get('/')
def get_all_users():
    return user.get_all_users()

@router.post('/')
def create_a_user():
    return user.create_a_user()

@router.get('/{uid}')
def query_a_user():
    return user.query_a_user()

@router.put('/{uid}')
def modify_a_user():
    return user.modify_a_user()

@router.delete('/{uid}')
def delete_a_user():
    return user.delete_a_user()

@router.get('/{uid}/device')
def get_user_devices_did():
    return user.get_user_devices_did()

@router.post('/{uid}/device')
def add_a_device_to_user():
    return user.add_a_device_to_user()

@router.delete('/{uid}/device')
def delete_a_device_from_user():
    return user.delete_a_device_from_user()