from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import ESPNPublicService, TabelaManager

app = FastAPI(title="Paulistão 2027 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API do Paulistão 2027 Rodando com Sucesso!"}

@app.get("/api/v1/tabela")
async def obter_tabela():
    try:
        dados_brutos = await ESPNPublicService.obter_partidas_formatadas()
        tabela_formatada = TabelaManager.formatar_tabela_classificacao(dados_brutos)
        return tabela_formatada
    except Exception as e:
        print(f"Erro ao gerar tabela: {e}")
        return []

@app.get("/api/v1/partidas")
async def obter_partidas(rodada: int = 1):
    try:
        partidas = await ESPNPublicService.obter_partidas_formatadas(rodada)
        return partidas
    except Exception as e:
        print(f"Erro ao buscar partidas: {e}")
        return []
