from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import hashlib

from routes.router import router

from src.db import Database
from src.security import create_access_token

@router.post("/token", tags=["Autenticação"], responses={
    200: {
        "description": "Autorizado", 
        "content": {
            "application/json": {"example": {"access_token":"xxx.yyy.zzz","token_type":"bearer"}}
        }
    },
    401: {
        "description": "Não autorizado", 
        "content": {
            "application/json": {"example": {"detail": "User or pass invalid"}}
        }
    },
    422: {
        "description": "Required filed is missing",
        "content": {
            "application/json": {"example": {"detail":[{"loc":["body","password"],"msg":"field required","type":"value_error.missing"}]}}
        }
    }
    })
async def criar_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    ## Realizar a solicitação do TOKEN, usando o padrão JSON Web Token.

    Argumentos obrigatórios:

        username (str): Usuário.
        password (str): Senha.

    Comando de teste:
        
        curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Accept: application/json" -d "username=admin&password=password" http://localhost:8000/token
    """
    db = Database()
    hash_senha = hashlib.sha256(form_data.password.encode('utf-8')).hexdigest()
    userObj = db.cnx.users.find_one({'username': form_data.username, 'password': hash_senha})
    if(not userObj):
        # NO USER
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User or pass invalid.")
    elif (not userObj['active']):
        # INACTIVE USER
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active. Please contact administrator.")
    else:
        # VALID USER
        session = {
            'id-user': userObj['_id'],
            'name': userObj['name'],
            'system-admin': userObj['system-admin'],
            'active': userObj['active']
        }
        access_token = create_access_token(data=session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"})