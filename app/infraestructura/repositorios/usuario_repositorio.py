from sqlalchemy.orm import Session

from app.dominio.modelos.usuario import Usuario
from app.infraestructura.basedatos.entidades.usuario_entidad import Usuario as UsuarioEntidad


class UsuarioRepositorio:
    def __init__(self, db: Session):
         self.db = db


    def crear_usuario(self, usuario: Usuario) -> UsuarioEntidad:
        usuario_creacion = UsuarioEntidad(**usuario.model_dump())
        self.db.add(usuario_creacion)
        self.db.commit()
        self.db.refresh(usuario_creacion)
        return usuario_creacion


    def obtener_usuario(self, usuario_id: str)-> UsuarioEntidad:
        return self.db.query(UsuarioEntidad).filter(UsuarioEntidad.id == usuario_id).first()


    def obtener_usuario_por_username(self, username: str)-> UsuarioEntidad:
        return self.db.query(UsuarioEntidad).filter(UsuarioEntidad.username == username).first()


    def actualizar_usuario(self, usuario_id: int, usuario: Usuario) -> UsuarioEntidad:
        usuario_db = self.obtener_usuario(usuario_id)
        if usuario_db:
            for key, value in usuario.dict(exclude_unset=True).items():
                setattr(usuario_db, key, value)
            self.db.commit()
            self.db.refresh(usuario_db)
        return usuario_db


    # def eliminar_usuario(self, usuario_id: int) -> UsuarioEntidad:
    #     usuario_db = self.obtener_usuario(usuario_id)
    #     if usuario_db:
    #         self.db.delete(usuario_db)
    #         self.db.commit()
    #     return usuario_db
