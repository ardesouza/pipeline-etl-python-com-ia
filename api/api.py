
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI(title="API de Clientes - Projeto ETL")

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "users.json"


def load_users():
    with open(DATABASE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    with open(DATABASE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


class NewsRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "API do projeto ETL funcionando!"}


@app.get("/users")
def get_users():
    return load_users()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    users = load_users()

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="Cliente não encontrado")


@app.put("/users/{user_id}/news")
def add_news(user_id: int, request: NewsRequest):
    users = load_users()

    for user in users:
        if user["id"] == user_id:
            user["news"].append(request.message)
            save_users(users)

            return {
                "message": "Notícia adicionada com sucesso",
                "user": user
            }

    raise HTTPException(status_code=404, detail="Cliente não encontrado")
