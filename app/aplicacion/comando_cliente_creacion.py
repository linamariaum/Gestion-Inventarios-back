from app.dominio.modelos.cliente import Cliente
from app.dominio.modelos.usuario import Usuario

class ClienteCreacion(Cliente, Usuario):
     password: str
