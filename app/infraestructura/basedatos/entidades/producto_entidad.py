from sqlalchemy import Column, Integer, String, ForeignKey

from app.infraestructura.basedatos.db import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Integer)
    cantidad = Column(Integer)

    idCategoria = Column(Integer, ForeignKey('categorias.id'))
    idCliente = Column(Integer, ForeignKey('clientes.id'))
