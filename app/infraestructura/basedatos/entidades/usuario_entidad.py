from sqlalchemy import Column, Integer, String

from app.infraestructura.basedatos.db import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    rol = Column(String)
    hashed_password = Column(String)
