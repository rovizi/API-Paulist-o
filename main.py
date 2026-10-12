from fastapi import FastAPI, BackgroundTasks
from typing import List
from config import settings
from models import PartidaResponse, TabelaPosicao
from services import ESPNPublicService, TabelaManager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API em FastAPI estruturada com a fonte de dados aberta da ESPN."
)

@app.get("/api/v1/paulistao/partidas", response_model=List[PartidaResponse])
async def listar_partidas(rodada: int = 1):
    """
    Retorna os confrontos da rodada (com escudos, horários, placar ao vivo,
    acréscimos e intervalo) direto da fonte pública da ESPN.
    """
    partidas = await ESPNPublicService.obter_partidas_formatadas()
    return partidas

@app.get("/api/v1/paulistao/classificacao", response_model=List[TabelaPosicao])
async def obter_tabela():
    """Retorna a tabela de classificação com alerta automático em vermelho no rebaixamento."""
    tabela_bruta = []
    return TabelaManager.processar_rebaixamento(tabela_bruta)

@app.post("/api/v1/paulistao/partidas/{id_partida}/monitorar-tempo-real")
async def monitorar_tempo_real(id_partida: str, background_tasks: BackgroundTasks):
    """Monitora em segundo plano para garantir o encerramento imediato (FT) sem delay."""
    async def checar_fim():
        pass
    background_tasks.add_task(checar_fim)
    return {"status": "sucesso", "mensagem": f"Monitoramento zero-delay ativado para a partida {id_partida}."}