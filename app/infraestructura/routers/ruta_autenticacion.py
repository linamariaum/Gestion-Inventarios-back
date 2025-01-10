from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated

from app.core.security import createToken, oauth2_scheme
from app.dominio.modelos.usuario import Usuario
from app.infraestructura.repositorios.usuario_repositorio import UsuarioRepositorio


routerLogin = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def autenticar_usuario(username: str, password: str) -> Usuario | bool: # TODO reubicar clase
    #user = UsuarioRepositorio.obtener_usuario(username) # Buscar si mi usuario existe en DB
    usuario = UsuarioRepositorio.fake_obtener_usuario(username)
    if not usuario:
        return False
    if not verificar_password(password, usuario['hashed_password']):
        return False
    return Usuario(**usuario)


@routerLogin.post('/',
        response_model=Token,
        summary="Login",
        description="Iniciar sesión",
        response_description="Obtiene token de autenticación")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Genera un Token de acceso para la cuenta cliente

    - **username**: requerido nombre de usuario
    - **password**: requerido contraseña de la cuenta
    """
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'mensaje': 'Usuario o contraseña incorrectos'},
            headers={'WWW-Authenticate': 'Bearer'}
        )
    usuario_logueado = Usuario(**usuario.model_dump())
    token = createToken(payload={'username': usuario_logueado.username, 'rol': usuario_logueado.rol})
    return Token(access_token=token, token_type="bearer")


@routerLogin.get('/',
        response_model=Token,
        summary="Obtener token activo",
        description="Obtener token activo",
        response_description="Obtiene token de autenticación")
async def obtener_token_activo(token: Annotated[str, Depends(oauth2_scheme)]):
    return Token(access_token=token, token_type="bearer")
