import logging

from fastapi import FastAPI

from app.auth import router as auth_router
from app.todo import router as todo_router
from app.user import router as user_router

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
)

app = FastAPI(title="Todo API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}
