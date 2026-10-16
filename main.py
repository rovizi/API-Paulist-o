from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import obter_tabela_paulistao, obter_partidas_paulistao

app = FastAPI(
    title="API Paulistão 2027",
    description="API híbrida com dados ao vivo da ESPN e escudos customizados.",
    version="1.0.0"
)

# Configuração de CORS para permitir acesso de qualquer origem (Looker Studio, painéis, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "online",
        "campeonato": "Paulistão 2027",
        "endpoints": {
            "tabela": "/api/v1/tabela",
            "partidas": "/api/v1/partidas"
        }
    }

@app.get("/api/v1/tabela")
def get_tabela():
    """Retorna a tabela de classificação atualizada com os escudos customizados."""
    return obter_tabela_paulistao()

@app.get("/api/v1/partidas")
def get_partidas():
    """Retorna as partidas da rodada com os escudos customizados dos mandantes e visitantes."""
    return obter_partidas_paulistao()
