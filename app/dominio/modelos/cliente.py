from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
    telefono: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
