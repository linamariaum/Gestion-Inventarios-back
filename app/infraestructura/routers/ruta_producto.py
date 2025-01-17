from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import csv
from io import StringIO

from app.core.security import validateToken
from app.dominio.modelos.producto import Producto
from app.aplicacion.comando_producto_creacion import ProductoCreacion
from app.infraestructura.basedatos.db import get_db
from app.infraestructura.repositorios.producto_repositorio import ProductoRepositorio
from app.infraestructura.repositorios.cliente_repositorio import ClienteRepositorio
from app.infraestructura.repositorios.categoria_repositorio import CategoriaRepositorio


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


@routerProductos.post('/carga-masiva',
    summary="Carga masiva de productos del cliente",
    description="Carga masiva de productos desde un archivo CSV",
    response_description="Carga masiva de productos",
    status_code=status.HTTP_201_CREATED
)
def crear_productos_carga_masiva(token_cliente: dict = Depends(validateToken), file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        columnas = {'nombre', 'idCategoria', 'precio', 'cantidad'}
        productos = []
        content = StringIO(file.file.read().decode('utf-8'))
        reader = csv.DictReader(content)
        if not columnas.issubset(reader.fieldnames):
            missing_columns = columnas - set(reader.fieldnames)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El archivo CSV no contiene las columnas necesarias: {', '.join(missing_columns)}")
        cliente = ClienteRepositorio(db=db).obtener_cliente(token_cliente.get('id'))
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')
        for row in reader:
            categoria_fila = int(row.get('idCategoria'))
            if not CategoriaRepositorio(db=db).existe_categoria(categoria_fila):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoría {str(categoria_fila)} no encontrada')
            producto = ProductoCreacion(
                nombre=row['nombre'],
                precio=int(row.get('precio')),
                cantidad=int(row.get('cantidad')),
                idCategoria=categoria_fila,
                idCliente=cliente.id
            )
            if not ProductoRepositorio(db=db).existe_producto_por_nombre_y_cliente(producto.nombre, producto.idCliente):
                productos.append(producto)
        if productos:
            ProductoRepositorio(db=db).crear_productos(productos)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'Productos cargados exitosamente'})
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error en la carga masiva de productos') from e
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error en el archivo CSV: columna {str(e)} no encontrada') from e
