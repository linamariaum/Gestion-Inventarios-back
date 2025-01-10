import datetime
from datetime import timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import os
import jwt


KEY_TOKEN = os.environ.get('KEY_TOKEN')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')


def createToken(payload: dict):
    to_encode = payload.copy()
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, key=KEY_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt


def validateToken(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        data = jwt.decode(token, key=KEY_TOKEN, algorithms=ALGORITHM)
        return data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expirado')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')


def validarRol(token: dict, rol: str) -> bool:
    if token['rol'] == rol:
        return True
    else:
        return False


def validarRolAdmin(token: dict = Depends(validateToken)) -> bool:
    es_admin = validarRol(token, 'admin')
    if not es_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos de administrador')
    return es_admin
