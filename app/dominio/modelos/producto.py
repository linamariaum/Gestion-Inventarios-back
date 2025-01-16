from pydantic import BaseModel
from typing import Optional
from app.dominio.modelos.categoria import Categoria

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    precio: int
    cantidad: int
    categoria: Optional[Categoria] = None

    class Config:
        orm_mode = True
        from_attributes = True
