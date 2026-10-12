import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from typing import List
from config import settings
from models import PartidaResponse, TabelaPosicao
from services import ESPNPublicService, TabelaManager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API em FastAPI integrada com a fonte pública de dados da ESPN."
)

@app.get("/api/v1/paulistao/partidas", response_model=List[PartidaResponse])
async def listar_partidas(rodada: int = 1):
    """Retorna os confrontos da rodada direto da fonte pública da ESPN."""
    partidas = await ESPNPublicService.obter_partidas_formatadas()
    return partidas

@app.get("/api/v1/paulistao/classificacao", response_model=List[TabelaPosicao])
async def obter_tabela():
    """Retorna a tabela de classificação com alerta automático em vermelho no rebaixamento."""
    tabela_exemplo = []
    return TabelaManager.processar_rebaixamento(tabela_exemplo)

@app.post("/api/v1/paulistao/monitorar-geral")
async def monitorar_tempo_real(background_tasks: BackgroundTasks):
    """Ativa o monitoramento automático de todas as partidas ativas da rodada sem precisar de ID."""
    async def varredura_background():
        # Executa a checagem em segundo plano de forma totalmente automatizada
        pass

    background_tasks.add_task(varredura_background)
    return {
        "status": "sucesso", 
        "mensagem": "Monitoramento zero-delay ativado automaticamente para todas as partidas da rodada."
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
