# -*- coding: utf-8 -*-

from fastapi import FastAPI
from services import obter_tabela_paulistao, obter_partidas_paulistao

# A instância 'app' que o uvicorn procura ao iniciar
app = FastAPI(
    title="API Paulistão 2027",
    description="API oficial com estatísticas e escudos padronizados dos 16 clubes da Série A1.",
    version="1.0.0"
)

@app.get("/")
def raiz():
    return {"mensagem": "API do Paulistão 2027 online e operante!"}

@app.get("/tabela")
def get_tabela():
    """Retorna a classificação atualizada com os escudos oficiais e dados zerados para o início do torneio."""
    return obter_tabela_paulistao()

@app.get("/partidas")
def get_partidas():
    """Retorna a lista de partidas injetando os escudos dos mandantes e visitantes."""
    return obter_partidas_paulistao()
