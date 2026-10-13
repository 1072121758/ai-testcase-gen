from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.security import get_current_user, hash_password

router = APIRouter()

# 模拟数据库：学习阶段先用内存字典，后面可换成 SQLite/MySQL
fake_users_db = {
    "wendi": {
        "username": "wendi",
        "email": "wendi@example.com",
        "password": hash_password("123456"),
    }
}


class UserOut(BaseModel):
    username: str
    email: str


@router.get("/users/me", response_model=UserOut)
def read_current_user(username: str = Depends(get_current_user)) -> UserOut:
    user = fake_users_db[username]
    return UserOut(username=user["username"], email=user["email"])
