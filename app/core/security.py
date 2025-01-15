import datetime
from datetime import timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os
import jwt

from app.dominio.modelos.usuario import Usuario
from app.infraestructura.basedatos.entidades.usuario_entidad import Usuario as UsuarioEntidad
from app.infraestructura.repositorios.usuario_repositorio import UsuarioRepositorio


KEY_TOKEN = os.environ.get('KEY_TOKEN')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No tiene permisos de administrador')
    return es_admin


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def autenticar_usuario(username: str, password: str, db: Session) -> Usuario | bool:
    usuario_db = UsuarioRepositorio(db=db).obtener_usuario_por_username(username=username)
    if not usuario_db:
        return False
    if not verificar_password(password, usuario_db.hashed_password):
        return False
    return Usuario(id=usuario_db.id, username=usuario_db.username, rol=usuario_db.rol)


def crearUsuario(username: str, password: str, rol: str, db: Session) -> Usuario:
    hash_password_create = hash_password(password)
    usuario_creacion = Usuario(username=username, rol=rol, hashed_password=hash_password_create)
    usuario_db: UsuarioEntidad = UsuarioRepositorio(db=db).crear_usuario(usuario_creacion)
    return Usuario.model_validate(usuario_db)
