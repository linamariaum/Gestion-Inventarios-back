from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dominio.modelos.producto import Producto
from app.aplicacion.comando_producto_creacion import ProductoCreacion
from app.infraestructura.basedatos.entidades.cliente_entidad import Cliente as ClienteEntidad
from app.infraestructura.basedatos.entidades.categoria_entidad import Categoria as CategoriaEntidad
from app.infraestructura.basedatos.entidades.producto_entidad import Producto as ProductoEntidad
from app.infraestructura.repositorios.cliente_repositorio import ClienteRepositorio
from app.infraestructura.repositorios.categoria_repositorio import CategoriaRepositorio


class ProductoRepositorio:
    def __init__(self, db: Session):
        self.db = db


    def obtener_productos(self, usuario_id: int) -> list[dict]:
        productos = (
            self.db.query(
                ProductoEntidad.id,
                ProductoEntidad.nombre,
                ProductoEntidad.precio,
                ProductoEntidad.cantidad,
                CategoriaEntidad.id.label('categoria_id'),
                CategoriaEntidad.nombre.label('categoria_nombre')
            )
            .join(ClienteEntidad, ClienteEntidad.id == ProductoEntidad.idCliente)
            .join(CategoriaEntidad, CategoriaEntidad.id == ProductoEntidad.idCategoria)
            .filter(ClienteEntidad.idUsuario == usuario_id)
            .all()
        )
        productos_con_categoria = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': producto.cantidad,
                'categoria': {
                    'id': producto.categoria_id,
                    'nombre': producto.categoria_nombre
                }
            }
            for producto in productos
        ]
        return productos_con_categoria


    def obtener_productos_por_categoria(self, usuario_id: int, categoria_id: int) -> list[ProductoEntidad]:
        productos = (
            self.db.query(ProductoEntidad)
            .join(ClienteEntidad, ClienteEntidad.id == ProductoEntidad.idCliente)
            .filter(ClienteEntidad.idUsuario == usuario_id, ProductoEntidad.idCategoria == categoria_id)
            .all()
        )
        return productos


    def obtener_producto_por_id(self, producto_id: int) -> ProductoEntidad:
        producto = self.db.query(ProductoEntidad).filter(ProductoEntidad.id == producto_id).first()
        return producto


    def producto_pertenece_cliente(self, usuario_id: int, producto_id: int) -> ProductoEntidad:
        cliente = ClienteRepositorio(self.db).obtener_cliente(usuario_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')
        producto_db = self.obtener_producto_por_id(producto_id)
        if not producto_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto no encontrado')
        if producto_db.idCliente != cliente.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto no pertenece al cliente')
        return producto_db


    def obtener_producto(self, usuario_id: int, producto_id: int) -> dict:
        producto_db = self.producto_pertenece_cliente(usuario_id, producto_id)
        categoria_producto = CategoriaRepositorio(self.db).obtener_categoria(producto_db.idCategoria)
        producto_db_categoria = {
                'id': producto_db.id,
                'nombre': producto_db.nombre,
                'precio': producto_db.precio,
                'cantidad': producto_db.cantidad,
                'categoria': {
                    'id': categoria_producto.id,
                    'nombre': categoria_producto.nombre
                }
            }
        return producto_db_categoria


    def crear_producto(self, producto_creacion: ProductoCreacion) -> ProductoEntidad:
        if not ClienteRepositorio(self.db).existe_cliente(producto_creacion.idCliente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')

        if not CategoriaRepositorio(self.db).existe_categoria(producto_creacion.idCategoria):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoría no encontrada')

        producto = ProductoEntidad(nombre=producto_creacion.nombre, precio=producto_creacion.precio, cantidad=producto_creacion.cantidad, idCliente=producto_creacion.idCliente, idCategoria=producto_creacion.idCategoria)
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto


    def crear_productos(self, productos: list[ProductoCreacion]) -> None:
        productos_entidades = [ProductoEntidad(nombre=producto.nombre, precio=producto.precio, cantidad=producto.cantidad, idCategoria=producto.idCategoria, idCliente=producto.idCliente) for producto in productos]
        self.db.bulk_save_objects(productos_entidades)
        self.db.commit()


    def actualizar_producto(self, usuario_id: int, producto_id: int, producto: Producto) -> ProductoEntidad:
        producto_db = self.producto_pertenece_cliente(usuario_id, producto_id)
        if producto_db:
            for key, value in producto.dict(exclude_unset=True).items():
                setattr(producto_db, key, value)
            self.db.commit()
            self.db.refresh(producto_db)
        return producto_db


    def existe_producto_por_nombre_y_cliente(self, nombre: str, id_cliente: int) -> bool:
        return self.db.query(ProductoEntidad).filter(ProductoEntidad.nombre == nombre, ProductoEntidad.idCliente == id_cliente).first() is not None
