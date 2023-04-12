from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
import json
from bson import json_util

from datetime import datetime, timedelta
import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict):
    session = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    session['exp'] = int(expire.timestamp())
    session = json.loads(json_util.dumps(session)) # Make JSON native
    encoded_jwt = jwt.encode(session, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        session = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        if int(session['exp']) < int(datetime.utcnow().timestamp()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
        return session
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")