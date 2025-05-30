from fastapi import FastAPI  # Framework para criacao da API
from fastapi.middleware.cors import CORSMiddleware  #  CORS para habilitar permissoes de uso da API
from contextlib import asynccontextmanager


from src.models import *  # Pre-carrega os modelos (tabelas) da base de dados
from src.routers import acesso_especial_routes, users_routers, constrole_acesso_router
from src.tasks.faltas_scheduler import iniciar_agendamentos 

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_agendamentos()
    yield


app = FastAPI(lifespan=lifespan)  # Inicia a aplicacao (Ponto inicial da API)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_routers.router)
app.include_router(acesso_especial_routes.router)
app.include_router(constrole_acesso_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server:app", reload=True)  # Inicia o servidor Uvicorn
