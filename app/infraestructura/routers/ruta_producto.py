from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.core.security import validateToken
from app.dominio.modelos.producto import Producto
from app.aplicacion.comando_producto_creacion import ProductoCreacion
from app.infraestructura.basedatos.db import get_db
from app.infraestructura.repositorios.producto_repositorio import ProductoRepositorio


routerProductos = APIRouter()


@routerProductos.get('/',
    response_model=List[Producto],
    summary="Obtener listado de productos",
    description="Lista los productos registrados de un cliente",
    response_description="Obtiene lista de productos"
)
def obtener_productos(token_cliente: dict = Depends(validateToken), db: Session = Depends(get_db)):
    productos_db = ProductoRepositorio(db=db).obtener_productos(token_cliente.get('id'))
    productos = [Producto.model_validate(producto) for producto in productos_db]
    return JSONResponse(content=jsonable_encoder(productos))


@routerProductos.get('/categoria/{categoria_id}',
    response_model=List[Producto],
    summary="Obtener listado de productos por categoría",
    description="Lista los productos registrados de un cliente por la categoría especificada",
    response_description="Obtiene lista de productos por categoría"
)
def obtener_productos_por_categoria(categoria_id: int, token_cliente: dict = Depends(validateToken), db: Session = Depends(get_db)):
    productos_db = ProductoRepositorio(db=db).obtener_productos_por_categoria(token_cliente.get('id'), categoria_id)
    productos = [Producto.model_validate(producto) for producto in productos_db]
    return JSONResponse(content=jsonable_encoder(productos))


@routerProductos.get('/{producto_id}',
    response_model=Producto,
    summary="Obtener un producto por su id",
    description="Retorna el producto por su id si pertenece al cliente autenticado",
    response_description="Obtiene el producto por su id"
)
def obtener_producto(producto_id: int, token_cliente: dict = Depends(validateToken), db: Session = Depends(get_db)):
    producto_db = ProductoRepositorio(db=db).obtener_producto(usuario_id=token_cliente.get('id'), producto_id=producto_id)
    return JSONResponse(content=jsonable_encoder(Producto.model_validate(producto_db)))


@routerProductos.post('/',
    response_model=Producto,
    dependencies=[Depends(validateToken)],
    summary="Crear producto de un cliente",
    description="Crea un producto del cliente en el sistema",
    response_description="Obtiene el producto creado"
)
def crear_producto(producto_creacion: ProductoCreacion, db: Session = Depends(get_db)):
    producto_nuevo = ProductoRepositorio(db=db).crear_producto(producto_creacion)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(Producto.model_validate(producto_nuevo)))


@routerProductos.put('/{producto_id}',
    response_model=Producto,
    summary="Actualizar producto de un cliente",
    description="Actualiza la información de un producto del cliente en el sistema",
    response_description="Obtiene el producto actualizado"
)
def actualizar_producto(producto_id: int, producto_actualizacion: Producto, token_cliente: dict = Depends(validateToken), db: Session = Depends(get_db)):
    producto = ProductoRepositorio(db=db).actualizar_producto(token_cliente.get('id'), producto_id, producto_actualizacion)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Producto.model_validate(producto)))
