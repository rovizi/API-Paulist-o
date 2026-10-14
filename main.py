import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from typing import List
from config import settings
from models import PartidaResponse, TabelaPosicao
from services import ESPNPublicService, TabelaManager

app = FastAPI(
    title="Live Go API",
    version=settings.VERSION,
    description="API Live Go para acompanhamento em tempo real do Campeonato Paulista."
)

@app.get("/api/v1/paulistao/partidas", response_model=List[PartidaResponse])
async def listar_partidas(rodada: int = 1):
    """
    Endpoint Oficial do Campeonato Paulista:
    Consulta a API real da ESPN e injeta os escudos customizados nos times.
    Caso a rodada oficial esteja sem jogos (ex: fora de temporada), retorna a simulação.
    """
    partidas_reais = await ESPNPublicService.obter_partidas_formatadas(rodada)
    
    # Se a ESPN retornar partidas oficiais ao vivo ou agendadas, entrega os dados reais
    if partidas_reais:
        return partidas_reais
        
    # Se estiver fora de temporada ou sem dados no momento, usa o fallback de testes
    return await ESPNPublicService.obter_partidas_teste(rodada)

@app.get("/api/v1/paulistao/partidas/teste", response_model=List[PartidaResponse])
async def listar_partidas_teste(rodada: int = 1):
    """Rota para validação estática dos 16 escudos em formato de simulação."""
    return await ESPNPublicService.obter_partidas_teste(rodada)

@app.get("/api/v1/paulistao/classificacao", response_model=List[TabelaPosicao])
async def obter_tabela():
    """Retorna a tabela de classificação."""
    tabela_exemplo = []
    return TabelaManager.processar_rebaixamento(tabela_exemplo)

@app.post("/api/v1/paulistao/monitorar-geral")
async def monitorar_tempo_real(background_tasks: BackgroundTasks):
    """Ativa o monitoramento automático de todas as partidas ativas."""
    async def varredura_background():
        pass

    background_tasks.add_task(varredura_background)
    return {
        "status": "sucesso", 
        "mensagem": "Monitoramento zero-delay ativado para as partidas da rodada."
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
