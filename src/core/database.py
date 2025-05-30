from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException


DATABASE_URL = ( # url para comunicacao com a bd
    "mssql+pyodbc://@DESKTOP-RN92I4G\\SQLEXPRESS/DB_Modulo_Facial"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Trusted_Connection=yes"
)

engine = create_engine(DATABASE_URL) # cria a comunicacao com a bd
SessionLocal = sessionmaker(autoflush=False, bind=engine) # sessao com a bd
Base = declarative_base() # Base para mapear as tabelas

def get_db(): # funcao para buscar a comunicacao com a bd
    try:
        db = SessionLocal()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Erro ao conectar à base de dados.")
    
    try:
        yield db
    finally:
        db.close()
