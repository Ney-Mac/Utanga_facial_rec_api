from fastapi import FastAPI  # Framework para criacao da API
from fastapi.middleware.cors import CORSMiddleware  #  CORS para habilitar permissoes de uso da API
from src.db_models import *  # Pre-carrega os modelos (tabelas) da base de dados

from src.routers import acesso_especial_routes
from src.routers import notas_routes
from src.routers import users_routers
from src.routers import turmas_router

# from src.routers import delete_user_router

app = FastAPI()  # Inicia a aplicacao (Ponto inicial da API)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_routers.router)
app.include_router(acesso_especial_routes.router)
app.include_router(notas_routes.router)
app.include_router(turmas_router.router)

# app.include_router(delete_user_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server:app", reload=True)  # Inicia o servidor Uvicorn
