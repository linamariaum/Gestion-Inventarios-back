# from sqlalchemy import Column, Integer, String
# from app.db.base_class import Base

# class EntidadUsuario(Base):
class UsuarioEntidad():
    __tablename__ = 'usuarios'

    id: str# = Column(Integer, primary_key=True, index=True)
    username: str# = Column(String, unique=True, index=True)
    hashed_password: str# = Column(String)
