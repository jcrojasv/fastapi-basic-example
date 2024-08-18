from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import contract_router as contracts
from config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solo el origen específico
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todas las cabeceras
)

app.include_router(contracts.router, prefix="/api/v1")