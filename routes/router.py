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
    document = {"gabeiel":"098"}
    db.insert_document('USERS', document)

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
