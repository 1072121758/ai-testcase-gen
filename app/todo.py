from itertools import count

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.security import get_current_user

router = APIRouter()

# 模拟数据库：id 自增
todo_db: dict[int, dict] = {}
_id_counter = count(start=1)


class TodoCreate(BaseModel):
    title: str


class TodoCreated(BaseModel):
    id: int
    title: str
    status: str = "created"


class TodoOut(BaseModel):
    id: int
    title: str


@router.post("/todos", response_model=TodoCreated, status_code=201)
def create_todo(
    body: TodoCreate,
    username: str = Depends(get_current_user),
) -> TodoCreated:
    todo = {"id": next(_id_counter), "title": body.title}
    todo_db[todo["id"]] = todo
    return TodoCreated(**todo)


@router.get("/todos", response_model=list[TodoOut])
def list_todos(username: str = Depends(get_current_user)) -> list[TodoOut]:
    return [TodoOut(**todo) for todo in todo_db.values()]
