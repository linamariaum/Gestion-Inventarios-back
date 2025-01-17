from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import validateToken, validarRolAdmin
from app.dominio.modelos.cliente import Cliente
from app.aplicacion.comando_cliente_creacion import ClienteCreacion
from app.infraestructura.basedatos.db import get_db
from app.infraestructura.repositorios.cliente_repositorio import ClienteRepositorio


routerClientes = APIRouter()


@routerClientes.post('/',
    response_model=Cliente,
    summary="Crear cliente",
    description="Crea un cliente si el usuario autenticado tiene permisos de administrador y lo registra en el sistema",
    response_description="Obtiene el cliente creado"
)
def crear_cliente(cliente_creacion: ClienteCreacion, permiso: Annotated[bool, Depends(validarRolAdmin)], db: Session = Depends(get_db)):
    """
    Retorna el cliente recien creado si el usuario autenticado tiene permisos de administrador

    - **Token**: requerido
    """
    if permiso:
        try:
            cliente_creacion.rol = 'cliente'
            cliente_nuevo = ClienteRepositorio(db=db).crear_cliente(cliente_creacion)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(Cliente.model_validate(cliente_nuevo)))
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El cliente ya existe') from e


@routerClientes.get('/all',
    response_model=List[Cliente],
    summary="Obtener listado de clientes",
    description="Lista los clientes registrados en el sistema si el usuario autenticado tiene permisos de administrador",
    response_description="Obtiene lista de clientes"
)
def obtener_clientes(permiso: Annotated[bool, Depends(validarRolAdmin)], db: Session = Depends(get_db)):
    """
    Retorna la lista de clientes si el usuario autenticado tiene permisos de administrador

    - **Token**: requerido
    """
    if permiso:
        clientes_db = ClienteRepositorio(db=db).obtener_clientes()
        clientes = [Cliente.model_validate(cliente) for cliente in clientes_db]
        return JSONResponse(content=jsonable_encoder(clientes))


@routerClientes.get('/', dependencies=[Depends(validateToken)],
    response_model=Cliente,
    summary="Obtener cliente autenticado",
    description="Devuelve la información del cliente",
    response_description="Obtiene el cliente autenticado"
)
def obtener_cliente(token_cliente: dict = Depends(validateToken), db: Session = Depends(get_db)):
    """
    Retorna la información del cliente autenticado

    - **Token**: requerido
    """
    usuario_id = token_cliente.get('id')
    cliente = ClienteRepositorio(db=db).obtener_cliente(usuario_id)
    if not cliente:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Cliente no encontrado'})
    return JSONResponse(content=jsonable_encoder(Cliente.model_validate(cliente)))
