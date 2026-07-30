from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import executions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SISCORP PCA - Automação de Cadastro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(executions.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
