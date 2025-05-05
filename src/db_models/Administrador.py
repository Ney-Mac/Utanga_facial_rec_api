from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.utils.NivelAdmin import NivelAdmin

class Administrador(Base):
    __tablename__ = "Administrador"
    
    id = Column(Integer, ForeignKey('Usuario.id'), primary_key=True)
    nivel = Column(Enum(NivelAdmin), nullable=False)
    
    usuario = relationship("Usuario", back_populates="administrador")
    