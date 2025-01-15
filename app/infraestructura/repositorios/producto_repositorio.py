from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dominio.modelos.producto import Producto
from app.aplicacion.comando_producto_creacion import ProductoCreacion
from app.infraestructura.basedatos.entidades.cliente_entidad import Cliente as ClienteEntidad
from app.infraestructura.basedatos.entidades.producto_entidad import Producto as ProductoEntidad
from app.infraestructura.repositorios.cliente_repositorio import ClienteRepositorio
from app.infraestructura.repositorios.categoria_repositorio import CategoriaRepositorio


class ProductoRepositorio:
    def __init__(self, db: Session):
        self.db = db


    def obtener_productos(self, usuario_id: int) -> list[ProductoEntidad]:
        productos = (
            self.db.query(ProductoEntidad)
            .join(ClienteEntidad, ClienteEntidad.id == ProductoEntidad.idCliente)
            .filter(ClienteEntidad.idUsuario == usuario_id)
            .all()
        )
        return productos


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


    def obtener_producto(self, usuario_id: int, producto_id: int) -> ProductoEntidad:
        return self.producto_pertenece_cliente(usuario_id, producto_id)


    def crear_producto(self, producto_creacion: ProductoCreacion) -> ProductoEntidad:
        if not ClienteRepositorio(self.db).existe_cliente(producto_creacion.idCliente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente no encontrado')

        if not CategoriaRepositorio(self.db).existe_categoria(producto_creacion.idCategoria):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoría no encontrada')

        producto = ProductoEntidad(**producto_creacion.model_dump())
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto


    def actualizar_producto(self, usuario_id: int, producto_id: int, producto: Producto) -> ProductoEntidad:
        producto_db = self.producto_pertenece_cliente(usuario_id, producto_id)
        if producto_db:
            for key, value in producto.dict(exclude_unset=True).items():
                setattr(producto_db, key, value)
            self.db.commit()
            self.db.refresh(producto_db)
        return producto_db
