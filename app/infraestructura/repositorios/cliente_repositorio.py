from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.dominio.modelos.usuario import Usuario
from app.dominio.modelos.cliente import Cliente
from app.aplicacion.comando_cliente_creacion import ClienteCreacion
from app.infraestructura.repositorios.usuario_repositorio import UsuarioRepositorio
from app.infraestructura.basedatos.entidades.cliente_entidad import Cliente as ClienteEntidad


class ClienteRepositorio:
    def __init__(self, db: Session):
        self.db = db


    def obtener_clientes(self) -> list[ClienteEntidad]:
        return self.db.query(ClienteEntidad).all()


    def obtener_cliente(self, usuario_id: int) -> ClienteEntidad:
        return self.db.query(ClienteEntidad).filter(ClienteEntidad.idUsuario == usuario_id).first()


    def crear_cliente(self, cliente_creacion: ClienteCreacion) -> ClienteEntidad:
        hash_password_create = hash_password(cliente_creacion.password)
        usuario_creacion = Usuario(username=cliente_creacion.username, hashed_password=hash_password_create, rol=cliente_creacion.rol)
        usuario_db = UsuarioRepositorio(self.db).crear_usuario(usuario_creacion)
        cliente = ClienteEntidad(id=cliente_creacion.id, nombre=cliente_creacion.nombre, email= cliente_creacion.email, telefono=cliente_creacion.telefono, idUsuario=usuario_db.id)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente


    def actualizar_cliente(self, usuario_id: int, cliente: Cliente) -> ClienteEntidad:
        cliente_db = self.obtener_cliente(usuario_id)
        if cliente_db:
            for key, value in cliente.dict(exclude_unset=True).items():
                setattr(cliente_db, key, value)
            self.db.commit()
            self.db.refresh(cliente_db)
        return cliente_db


    def existe_cliente(self, cliente_id: int) -> bool:
        return self.db.query(ClienteEntidad).filter(ClienteEntidad.id == cliente_id).first() is not None
