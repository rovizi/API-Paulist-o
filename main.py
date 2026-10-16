# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import obter_tabela_paulistao, obter_partidas_paulistao

app = FastAPI(
    title="API Paulistão 2027",
    description="API oficial com estatísticas e escudos padronizados dos 16 clubes da Série A1.",
    version="1.0.0"
)

# Configuração de CORS para permitir requisições de qualquer front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {"mensagem": "API do Paulistão 2027 online e operante!"}

@app.get("/api/v1/tabela")
def get_tabela():
    """Retorna a classificação atualizada com os escudos oficiais."""
    return obter_tabela_paulistao()

@app.get("/api/v1/partidas")
def get_partidas():
    """Retorna a lista de partidas do campeonato."""
    return obter_partidas_paulistao()
