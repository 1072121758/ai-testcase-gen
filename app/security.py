from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from hashlib import sha256

# 学习项目用固定密钥；真实项目应放到环境变量里
SECRET_KEY = "change-me-to-a-random-secret-in-production!"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

# tokenUrl 指向 OAuth2 表单登录接口，Swagger 文档里可以直接点 Authorize 登录
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    """验证 token，返回其中的用户名；无效则抛 401"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效 Token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """依赖注入：从 Authorization: Bearer xxx 中解析出当前用户名"""
    return decode_token(token)
