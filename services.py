import httpx
from typing import List, Dict, Any
from config import settings

class ESPNPublicService:
    """Faz as requisições diretas na API pública e aberta da ESPN."""

    @staticmethod
    async def buscar_dados_espn() -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(settings.ESPN_PAULISTA_URL, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Erro ao conectar com a fonte da ESPN: {e}")
        return {}

    @classmethod
    async def obter_partidas_formatadas(cls) -> List[Dict[str, Any]]:
        dados = await cls.buscar_dados_espn()
        eventos = dados.get("events", [])
        
        partidas_processadas = []
        for ev in eventos:
            # Lógica de mapeamento dos dados vindos do JSON público da ESPN
            pass
            
        return partidas_processadas

class TabelaManager:
    """Calcula a classificação e aplica a regra visual de rebaixamento (vermelho)."""

    @staticmethod
    def processar_rebaixamento(tabela_crua: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        total = len(tabela_crua)
        for idx, item in enumerate(tabela_crua):
            pos = idx + 1
            # Marca os últimos colocados em vermelho na zona de rebaixamento
            zona = "rebaixamento" if pos >= (total - 1) else "normal"
            item["posicao"] = pos
            item["zona"] = zona
            item["cor_destaque"] = "vermelho" if zona == "rebaixamento" else "neutro"
        return tabela_crua