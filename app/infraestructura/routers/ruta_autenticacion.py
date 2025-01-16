from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from app.core.security import createToken, oauth2_scheme
from app.core.security import autenticar_usuario, crearUsuario
from app.dominio.modelos.usuario import Usuario
from app.infraestructura.basedatos.db import get_db


routerLogin = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str
    rol: Optional[str] = None


@routerLogin.post('/',
        response_model=Token,
        summary="Login",
        description="Iniciar sesión",
        response_description="Obtiene token de autenticación")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    """
    Autentica el usuario en el sistema y genera un Token de acceso para la cuenta

    - **username**: requerido nombre de usuario
    - **password**: requerido contraseña de la cuenta
    """
    usuario_logueado = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario_logueado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario o contraseña incorrectos',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    token = createToken(payload={'id': usuario_logueado.id, 'rol': usuario_logueado.rol})
    return Token(access_token=token, token_type="bearer", rol=usuario_logueado.rol)


@routerLogin.get('/',
        response_model=Token,
        summary="Obtener token activo",
        description="Obtener token activo",
        response_description="Obtiene token de autenticación")
async def obtener_token_activo(token: Annotated[str, Depends(oauth2_scheme)]):
    return Token(access_token=token, token_type="bearer")


@routerLogin.post('/crearUsuario',
    include_in_schema=False,
    response_model=Usuario
)
def crear_usuario(username: str = Body(), password: str = Body(), rol: str = Body(), db: Session = Depends(get_db)):
    try:
        rol = 'admin'
        usuario_nuevo = crearUsuario(username, password, rol, db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(usuario_nuevo))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario ya existe') from e
