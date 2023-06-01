from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional, Union
from passlib.context import CryptContext

app = FastAPI()
users_db = {}
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # パスワードのハッシュ化

class UserIn(BaseModel):
    user_id: str = Field(..., min_length=6, max_length=20, regex="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8, max_length=20, regex="^[a-zA-Z0-9_-]+$")

class UserOut(BaseModel):
    user_id: str
    nickname: str

class ErrorResponse(BaseModel):
    message: str
    cause: Optional[str] = None


# POST/signup
@app.post("/signup", response_model=Union[UserOut, ErrorResponse], status_code=200)
async def signup(user: UserIn):
    user_id = user.user_id
    password = user.password
    print(user_id)
    print(password)
    
    # ユーザー登録済みの場合
    if user_id in users_db:
        return ErrorResponse(
            message="Account creation failed",
            cause="already same user_id is used"
        ), 400

    try:
        #hashed_password = pwd_context.hash(password)   # パスワードをハッシュ化
        users_db[user_id] = {"nickname": user_id, "password": password}   # DBへ格納
        return {
                "message": "Account successfully created",
                "user": {
                    "user_id": user_id, "nickname": user_id
                }
            }
    except ValidationError as e:
        return ErrorResponse(
            message="Account creation failed",
            cause=str(e.errors())
        ), 400
