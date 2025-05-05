from fastapi import FastAPI
from routers import login_routes
from src.db_models import *
from routers.adm_routes import cadastro_routes, turmas_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get('/')
def welcome():
    return "No ar!"

app.include_router(login_routes.router)
app.include_router(cadastro_routes.router)
app.include_router(turmas_routes.router)
