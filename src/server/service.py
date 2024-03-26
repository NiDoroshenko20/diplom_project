import fastapi
import peewee
from src.server.database.database_models import BaseModel
from src.server.database.pydantic_models import ModifyBaseModel
from typing import Type


class RouterManager:
    def __init__(self, object_name: str, pydantic_model: Type[ModifyBaseModel], database_model: Type[BaseModel], prefix: str, tags: list[str]):
        self.object_name = object_name
        self.pydantic_model = pydantic_model
        self.database_model = database_model
        self.fastapi_router: fastapi.APIRouter = fastapi.APIRouter(prefix=prefix, tags=tags)
        self.resolver_manager = ResolverManager(self.database_model, self.pydantic_model)
        self.__init_methods()
    
    def __init_methods(self) -> None:
        @self.fastapi_router.get(path='/{id}', response_model=dict)
        def get(id: int) -> dict:
            return self.resolver_manager.get(id)
        
        @self.fastapi_router.get(path='/', response_model=dict)
        def get_all() -> dict:
            return self.resolver_manager.get_all()
        
        @self.fastapi_router.post(path='/', response_model=dict)
        def new(data: self.pydantic_model) -> dict:
            return self.resolver_manager.new(data)
        
        @self.fastapi_router.put(path='/{id}', response_model=dict)
        def update(id: int, data: self.pydantic_model) -> dict:
            return self.resolver_manager.update(id, data)
        
        @self.fastapi_router.delete(path='/{id}', response_model=dict)
        def delete(id: int) -> dict:
            return self.resolver_manager.delete(id)


class ResolverManager:
    def __init__(self, database_model: Type[BaseModel], pydantic_model: Type[ModifyBaseModel]) -> None:
        self.database_model = database_model
        self.pydantic_model = pydantic_model

    def check_for_errors(self) -> dict:
        try:
            self.check_fun()
            return {'code': 200, 'msg': 'Succesfully', 'result': False}
        except peewee.DoesNotExist:
            return {'code': 201, 'msg': 'Error for check', 'result': False}
        except:
            return {'code': 400, 'msg': 'Error', 'result': True}
        
    def check_fun(self, id=-1):
        return self.database_model.get(self.database_model.id == id)
    
    def get(self, id: int) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        
        res = self.database_model.get_or_none(self.database_model.id == id)
            
        return {'code': 200, 'msg': 'Succesfully', 'result': res.__data__} if res else {'code': 400, 'msg': 'Not found', 'result': None}
    
    def get_all(self) -> dict:
        check = self.check_for_errors()
        if check["result"]:
            return check
        
        models_list = []

        for model in self.database_model.select():
            new_model = {}

            for attr in model.__data__:
                get_attr = getattr(model, attr)

                new_model[attr] = get_attr

            models_list.append(new_model)
        
        return {'code': 200, 'msg': "Succesfully", 'result': models_list} if len(models_list) > 0 else {'code': 400, 'msg': 'Not found', 'result': None}
    
    def new(self, new_model: Type[ModifyBaseModel]) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        
        new_database_model = self.database_model.create()

        for attr in dir(new_model):
            if attr.startswith('__') or attr.startswith('id'):
                continue

            setattr(new_database_model, attr, getattr(new_model, attr))

        new_database_model.save()

        return self.get(new_database_model.id)
    
    def update(self, id: int, new_model: Type[ModifyBaseModel]) -> None:
        check = self.check_for_errors()
        if check['result']:
            return check
        
        database_model = self.database_model.get_or_none(self.database_model.id == id)

        if not database_model:
            return {'code': 400, 'msg': 'Not found', 'result': None}
        
        for attr in dir(new_model):
            if attr.startswith('__') or attr.startswith('id'):
                continue

            setattr(database_model, attr, getattr(new_model, attr))

        database_model.save()

        return {'code': 200, 'msg': 'Succesfully', 'result': self.get(database_model.id)['result']}
    
    def delete(self, id: int) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        
        res = self.database_model.get_or_none(self.database_model.id == id)

        if res:
            res.delete_instance()
        
        return {'code': 200, 'msg': 'Succesfully', 'result': None} if res else {'code': 400, 'msg': 'Not found', 'result': None}