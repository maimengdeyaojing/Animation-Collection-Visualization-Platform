from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if db_user:
        raise HTTPException(
            status_code=409,
            detail="用户名已存在"
        )

    db_user = User(
        username=user.username,
        #password=user.password,
        password=hash_password(user.password),
        email=user.email
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return {
        "message": "注册成功"
    }

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="用户不存在"
        )

    # if db_user.password != user.password:
    if not verify_password(user.password,db_user.password):
        raise HTTPException(
            status_code=401,
            detail="密码错误"
        )

    # return {
    #     "message": "登录成功",
    #     "username": db_user.username
    # }
    token = create_access_token(
    {
        "sub": db_user.username
    }
    )

    return {
        "message": "登录成功",
        "username": db_user.username,
        "token": token
    }

@router.get("/me")
def get_me(
    username: str = Depends(get_current_user)
):

    return {
        "username": username
    }
