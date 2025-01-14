from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    username: str
    rol: str
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
