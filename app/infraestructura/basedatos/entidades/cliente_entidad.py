from sqlalchemy import Column, Integer, String, ForeignKey

from app.infraestructura.basedatos.db import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    email = Column(String)
    telefono = Column(String)

    idUsuario = Column(Integer, ForeignKey('usuarios.id'))
