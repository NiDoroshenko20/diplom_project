from src.server.database import pydantic_models, database_models
from src.server.service import RouterManager

clients = RouterManager(object_name='clients', pydantic_model=pydantic_models.Client, database_model=database_models.Client, prefix='/clients', tags=['Clients'])
posts = RouterManager(object_name='posts', pydantic_model=pydantic_models.Post, database_model=database_models.Post, prefix='/posts', tags=['Posts'])
visits = RouterManager(object_name='visits',pydantic_model=pydantic_models.Visits, database_model=database_models.Visits, prefix='/visits', tags=['Visits'])
services = RouterManager(object_name='services', pydantic_model=pydantic_models.Services, database_model=database_models.Services, prefix='/services', tags=['Services'])
users = RouterManager(object_name='users', pydantic_model=pydantic_models.User, database_model=database_models.User, prefix='/users', tags=['Users'])
workers = RouterManager(object_name='workers', pydantic_model=pydantic_models.Workers, database_model=database_models.Workers, prefix='/workers', tags=['Workers'])


routers = (
    clients, 
    posts, 
    visits, 
    services, 
    users, 
    workers
)
