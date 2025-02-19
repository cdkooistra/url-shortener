# auth logic here:
# verify credentials

from sqlmodel import Session, select
from auth.models import UserModel, SessionDep
from auth.utils import hash_password, verify_password
from auth.jwt import create_jwt

# Creates a new user if the username is unique.
def create_user(username: str, password: str, session: SessionDep) -> bool:

    user = session.exec(select(UserModel).where(UserModel.username == username)).first()
    
    if user:
        return False
    
    new_user = UserModel(username=username, password_hash=hash_password(password))
    session.add(new_user)
    session.commit()
    return True

# Verifies if the username exists and password is correct.
def verify_user(username: str, password: str, session: SessionDep) -> bool:

    user = session.exec(select(UserModel).where(UserModel.username == username)).first()
    
    if user and verify_password(password, user.password_hash):
        payload = {"sub": username} # jwt payload with username
        return create_jwt(payload) # returns jwt when verified
    
    return False

# Updates password if the old password is correct.
def update_password(username: str, old_password: str, new_password: str, session: SessionDep) -> bool:

    user = session.exec(select(UserModel).where(UserModel.username == username)).first()
    
    if user and verify_password(old_password, user.password_hash):
        user.password_hash = hash_password(new_password)
        session.commit()
        return True
    
    return False