from pydantic import BaseModel
from src.utils.TipoUsuario import TipoUsuario
from typing import Optional

class UserResponse(BaseModel):
    id: int
    nome: str
    tipo: TipoUsuario
    codigo_acesso: str
    curso: Optional[str] = None
    departamento: Optional[str] = None
    nivel: Optional[str] = None
    
class AuthResponse(BaseModel):
    message: str
    user: UserResponse