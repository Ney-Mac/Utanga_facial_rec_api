from sqlalchemy import Column, String
from src.core.database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(String(20), primary_key=True)
    face_encodings = Column(String, nullable=False)
