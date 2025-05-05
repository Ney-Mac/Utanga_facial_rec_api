from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException


DATABASE_URL = (
    "mssql+pyodbc://@DESKTOP-RN92I4G\\SQLEXPRESS/DB_System_Utanga"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Trusted_Connection=yes"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Erro ao conectar à base de dados.")
    
    try:
        yield db
    finally:
        db.close()
