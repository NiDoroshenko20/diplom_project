from src.server.database import pydantic_models, database_models


def login(login: str, password: str) -> dict:
    res = database_models.User.get_or_none(database_models.User.login == login, database_models.User.password == password)
    
    return {"code": 200, 'msg': 'Succesfully', 'result': pydantic_models.User(
        id=res.id,
        login=res.login,
        position=res.position,
        password=res.password,
        power_level=res.power_level
    )} if res else {'code': 400, 'msg': 'Not found', 'result': None}

def change_password(id: int, password: str) -> dict:
    res = database_models.User.get_or_none(database_models.User.id == id)

    res.password = password

    res.save()

    return {'code': 200, 'msg': 'Succesfully', 'result': True}