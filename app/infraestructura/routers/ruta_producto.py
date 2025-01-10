from fastapi import APIRouter

routerProductos = APIRouter()

@routerProductos.get('/')
def obtener_productos():
    return {'mensaje': 'Get de productos'}
