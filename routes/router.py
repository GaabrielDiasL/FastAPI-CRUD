from fastapi import APIRouter, Body, HTTPException, status
from bson.objectid import ObjectId
import json
from fastapi.encoders import jsonable_encoder

from config.db import Database

from models.users import User

router = APIRouter()

#CRUD Application

#Create
@router.post("/new_user")
async def new_user(user: User):
    db = Database()
    document = {"name":user.name,"password":user.password}
    db.insert_document('USERS', document)
    return {"message":"Success"}


#Read
@router.get("/users")
async def get_users():
    db = Database()
    try:
        users = db.cnx["USERS"]
        user = [json.loads(json.dumps(document, default=str)) for document in users.find({})]
        data = []
        for document in user:
            data.append(document['name'])
        return data
    except:
        return {"Erro":"Conexão com banco de dados não realizada!"}

#Update
@router.put("/users/{user_name}")
async def update_user(user: User, user_name: str):
    db  = Database()
    existing_user = db.find_item('USERS', user_name)
    print(existing_user)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"Resposta": "Ok"}

#Teste select
@router.get("/teste")
async def testa():
    db = Database()
    users = db.cnx['USERS']
    testa = db.find_item('USERS','gabriel')
    print(testa)