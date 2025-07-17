import time

from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel
from authx import AuthX, AuthXConfig



app = FastAPI()  # Создал приложение

config = AuthXConfig()  # Создал объект конфигурационный
config.JWT_SECRET_KEY = "MY_SECRET_KEY"  # Добавил в config некоторые значения
config.JWT_ACCESS_COOKIE_NAME = "MY_ACCESS_TOKEN"  # Добавил в config Имя нашего токена, которое будет видно в cookie
config.JWT_TOKEN_LOCATION = ["cookies"]  # Добавил в config где будет храниться наш токен(по дефолту в headers)

security = AuthX(config=config)  # Создали ещё объект и передали ему наш объект, который создали ранее


# Схема наших данных, созданных с помощью pydantic -> BaseModel
class UserLogingSchema(BaseModel):
    username: str
    password: str
    unique_identifier: str




@app.post("/login")
def login(data_with_name_password_uid: UserLogingSchema, response: Response):
    if data_with_name_password_uid.username == "root" and data_with_name_password_uid.password == "root":
        token = security.create_access_token(data_with_name_password_uid.unique_identifier)
        print(time.time())
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=True,  # В production должно быть True
        )
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="incorrect username or password")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"secret_data": "WORLD_SECRET"}