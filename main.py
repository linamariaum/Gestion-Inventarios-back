from fastapi import FastAPI
from app.infraestructura.routers.ruta_autenticacion import routerLogin
from app.infraestructura.routers.ruta_cliente import routerClientes
from app.infraestructura.routers.ruta_producto import routerProductos

app = FastAPI(
    title='Gestion Inventarios API',
    description='API para el manejo de inventario de los distintos clientes',
    version='0.0.1'
)

@app.get('/api', tags=['Inicio'])
def bienvenida():
    return {'mensaje': 'Bienvenidos a Gestion Inventarios ms'}

app.include_router(routerLogin, tags=['Autenticacion'], prefix='/api/v1/login')
app.include_router(routerClientes, tags=['Clientes'], prefix='/api/v1/clientes')
app.include_router(routerProductos, tags=['Productos'], prefix='/api/v1/productos')
