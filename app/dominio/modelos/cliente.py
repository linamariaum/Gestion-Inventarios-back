from pydantic import BaseModel
from typing import List, Optional

class Cliente(BaseModel):
    id: int
    username: str
    nombre: str
    email: str
    telefono: Optional[str] = None
    inventories: List[int] = []




# Inventario
#     idIventario
#     idCliente
#     sede
#     fechaCreacion
#     fechaActualizacion
#     idStock


# Stock
#     idStock
#     idProducto
#     cantidad


# Producto
#     idProducto
#     idCliente
#     nombre
#     precio
#     categoria
#     marca


# Trazabilidad
#     idTrazabilidad
#     idCliente
#     idStock
#     idProducto
#     cantidad
#     fechaHora


# 1   Cliente 01  iphone  10  lunes10pm
# 2   Cliente 01  iphone  8   lunes10:05pm


# Usuario
#     admins(Logy)
#     Clines
