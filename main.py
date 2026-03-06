import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

APP_NAME= os.getenv("APP_NAME","Simple API")
APP_ENV=os.getenv("APP_ENV","local")

origins_env=os.getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS: List[str]=[o.strip() for o in origins_env.split(",") if o.split()] or ["*"]


app=FastAPI(title=APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class AddRequest(BaseModel):
    a: int
    b: int

class AddResponse(BaseModel):
    result: int


@app.get("/health")
def health():
    return {"status": "ok", "env":APP_ENV}

@app.post("/add", response_model=AddResponse)
def add_numbers(payload: AddRequest ):
    return {"result": payload.a + payload.b}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="item_id must be > 0")
    return {"item_id": item_id, "name": f"Item-{item_id}"}     