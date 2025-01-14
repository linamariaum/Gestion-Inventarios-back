from sqlalchemy import Column, Integer, String

from app.infraestructura.basedatos.db import Base


class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
