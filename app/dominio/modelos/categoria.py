from pydantic import BaseModel
from typing import Optional


class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str

    class Config:
        orm_mode = True
        from_attributes = True
