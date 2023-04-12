from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import Field

from bson.objectid import ObjectId
import json
import hashlib

from src.db import Database
from models.users import User, UpdateUser
from src.security import oauth2_scheme, verify_token

import config

router = APIRouter()

#CRUD Application

#Create
@router.post("/new_user", tags=['CRUD'])
async def new_user(user: User, token=Depends(oauth2_scheme)):
    session = verify_token(token)
    try:
        new_user_payload = {
            "username":user.username,
            "password": hashlib.sha256(user.password.encode('utf-8')).hexdigest(),
            "name": user.name,
            "system-admin": user.system_admin,
            "active": True
        }

        db = Database()
        inserted_id = db.cnx.users.insert_one(new_user_payload).inserted_id
        new_user_payload["_id"] = str(new_user_payload["_id"])

        success_return_payload = {
            "status_code": 201,
            "message": "User created successfully",
            "data": {
                "_id": new_user_payload["_id"],
                "username": new_user_payload["username"],
                "system-admin": new_user_payload["system-admin"],
            }
        }

        return success_return_payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "status_code": 400,
            "message": "User could not be created. Try again later.",
            "data": {
                "log": str(e)
            }
        })

#Read
@router.get("/get/users", tags=['CRUD'])
async def get_users(token=Depends(oauth2_scheme)):
    session = verify_token(token)
    db = Database()
    try:
        db_users = db.cnx['users']
        user = [json.loads(json.dumps(document, default=str)) for document in db_users.find({})]
        user_data_found = []
        for document in user:
            item = {}
            item['_id'] = str(document.get('_id'))
            item['username'] = document.get('username')
            item['name'] = str(document.get('name'))
            item['system-admin'] = document.get('system-admin')
            item['active'] = document.get('active')
            user_data_found.append(item)
        
        success_return_payload = {
            "status_code": 200,
            "message": "Users found: {}".format(len(user_data_found)),
            "data": user_data_found
        }

        return success_return_payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "status_code": 400,
            "message": "Users could not be retrieved",
            "data": {
                "log": str(e)
            }
        })

#Update
@router.put("/update/users/{username}", tags=['CRUD'])
async def update_user(user: UpdateUser, username: str, token=Depends(oauth2_scheme)):
    session = verify_token(token)
    """
    ## This route is responsible for update user data.

    Please, provide only the information that you want to update. Don't fill the json payload with information you want to keep.
    """
    db  = Database()
    existing_user = db.cnx.users.find_one({"username": username})

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status_code": 404,
            "message": "User not found",
            "data": {}
        })
    else:
        existing_user['_id'] = str(existing_user['_id'])
        user_json = user.dict(exclude_unset=True, exclude_none=True)
        
        if len(user_json) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "status_code": 404,
                "message": "Please, provide some info to update in the selected user.",
                "data": {}
            })

        new_user_data = {}
        if user.username:
            new_user_data['username'] = user.username
        if user.name:
            new_user_data['name'] = user.name

        db.cnx.users.update_one({"_id": ObjectId(existing_user["_id"])}, {"$set": new_user_data})

        success_return_payload = {
            "status_code": 200,
            "message": "User successfully updated",
            "data": {
                "_id": existing_user['_id'],
                "new_user_data": new_user_data
            }
        }
        return success_return_payload

#Delete
@router.delete("/delete/{username}", tags=['CRUD'])
async def delete_username(username: str, token=Depends(oauth2_scheme)):
    session = verify_token(token)
    db = Database()
    users = db.cnx['users']
    existing_user = users.find_one({"username": username})

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status_code": 404,
            "message": "User not found",
            "data": {}
        })
    else:
        users.delete_one({"username": username})

        success_return_payload = {
            "status_code": 200,
            "message": "User successfully deleted",
            "data": {}
        }
        return success_return_payload