from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    precio: int
    cantidad: int

    class Config:
        orm_mode = True
        from_attributes = True
