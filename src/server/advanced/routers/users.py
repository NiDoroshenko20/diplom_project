from src.server.router import routers
from src.server.database.pydantic_models import LoginData, ChangePassword
from src.server.advanced.resolvers import users

user_router = routers[4]
print(user_router)

@user_router.fastapi_router.post(path='/login', response_model=dict)
def login(data: LoginData) -> dict:
    return users.login(data.login, data.password)

@user_router.fastapi_router.put(path='/change_password/{id}', response_model=dict)
def change_password(id: int, data: ChangePassword):
    return users.change_password(id, data.password)