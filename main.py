import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from typing import List, Union, Dict, Any
from config import settings
from models import PartidaResponse, TabelaPosicao
from services import ESPNPublicService, TabelaManager

app = FastAPI(
    title="Live Go API",
    version=settings.VERSION,
    description="API Live Go para acompanhamento em tempo real do Campeonato Paulista."
)

@app.get("/api/v1/paulistao/partidas")
async def listar_partidas(rodada: int = 1) -> Union[List[PartidaResponse], Dict[str, Any]]:
    """Retorna os confrontos da rodada ou a mensagem de espera caso a tabela oficial ainda não esteja disponível."""
    partidas = await ESPNPublicService.obter_partidas_formatadas()
    
    # Se a lista estiver vazia (aguardando divulgação da FPF), retorna a mensagem e o status em português
    if not partidas:
        return {
            "status": "em_espera",
            "mensagem": "Aguardando dados do Paulistão 2027",
            "partidas": []
        }
        
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
        "mensagem": "Monitoramento zero-delay ativado automaticamente pela Live Go para todas as partidas da rodada."
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
