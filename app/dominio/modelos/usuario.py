from pydantic import BaseModel

class Usuario(BaseModel):
    username: str
    rol: str
    hashed_password: str
