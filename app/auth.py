from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.security import create_access_token, hash_password
from app.user import fake_users_db

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def _authenticate(username: str, password: str) -> TokenResponse:
    user = fake_users_db.get(username)
    if not user or user["password"] != hash_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    return TokenResponse(access_token=create_access_token(username))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    """JSON 登录（按接口设计文档的格式）"""
    return _authenticate(body.username, body.password)


@router.post("/auth/token", response_model=TokenResponse)
def auth_token(form: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """表单登录（OAuth2 标准格式，Swagger 的 Authorize 弹窗走这个）"""
    return _authenticate(form.username, form.password)
