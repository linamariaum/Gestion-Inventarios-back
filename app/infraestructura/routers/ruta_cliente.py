from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import Annotated, List

from app.core.security import validateToken, validarRolAdmin
from app.dominio.modelos.cliente import Cliente


routerClientes = APIRouter()

fake_clientes_db = [
    {
        "id": 1,
        "username": "johndoe",
        "nombre": "Almacenes Exito SA",
        "email": "exito@email.com",
        "telefono": "12354668979",
        "inventories": []
    },
    {
        "id": 2,
        "username": "jumbo",
        "nombre": "Almacenes JUMBO SA",
        "email": "jumbo@email.com",
        "telefono": "23166656",
        "inventories": []
    }
]


@routerClientes.get('/all',
    response_model=List[Cliente],
    summary="Obtener listado de clientes",
    description="Lista los clientes registrados en el sistema",
    response_description="Obtiene lista de clientes"
)
def obtener_clientes(permiso: Annotated[bool, Depends(validarRolAdmin)]):
    if permiso:
        return JSONResponse(content=fake_clientes_db)


def fake_obtener_cliente(token_cliente: dict = Depends(validateToken)) -> Cliente | None:
    username = token_cliente.get('username')
    print("Entre a obtener fake con ", username)
    for cliente in fake_clientes_db:
        print('clientecistoooooooooo', cliente)
        if cliente['username'] == username:
            return Cliente(**cliente)
    return None


@routerClientes.get('/', dependencies=[Depends(validateToken)],
    summary="Obtener cliente autenticado",
    description="Devuelve la información del cliente",
    response_description="Obtiene el cliente autenticado"
)
def obtener_cliente_id(cliente: Annotated[Cliente, Depends(fake_obtener_cliente)]):
    if not cliente:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={'mensaje': 'Cliente no encontrado'})
    return cliente


