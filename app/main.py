import logging

from app.user import User
from fastapi import FastAPI


logging.basicConfig(
    filename="app.log",
    level=logging.INFO
)


app = FastAPI()


@app.get("/")
def read_root():

    user = User(
        "Wendi",
        "wendi@example.com"
    )

    logging.info(
        f"user access: {user.name}"
    )

    return f"Hello {user.name}!Welcome to Todo API"