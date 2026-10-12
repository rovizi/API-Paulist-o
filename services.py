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
        eventos_espn = dados.get("events", [])
        
        partidas_processadas = []
        
        for idx, evento in enumerate(eventos_espn):
            competicao = evento.get("competitions", [{}])[0]
            status_obj = evento.get("status", {}).get("type", {})
            status_sigla = status_obj.get("state", "pre") # pre, in, post
            
            # Mapeamento de status para o seu padrão
            if status_sigla == "pre":
                status = "NS"
                status_desc = "Agendado"
            elif status_sigla == "in":
                status = "LIVE"
                status_desc = "Em andamento"
            else:
                status = "FT"
                status_desc = "Encerrado"
            
            concorrentes = competicao.get("competitors", [])
            mandante_info = {}
            visitante_info = {}
            
            for c in concorrentes:
                if c.get("homeAway") == "home":
                    mandante_info = c
                else:
                    visitante_info = c

            # Extração dos dados e escudos
            partida = {
                "id_partida": str(evento.get("id", idx + 1)),
                "rodada": 1,
                "status": status,
                "status_descricao": status_desc,
                "data_hora": evento.get("date", ""),
                "estadio": competicao.get("venue", {}).get("fullName", "Estádio a definir"),
                "mandante": mandante_info.get("team", {}).get("displayName", "Mandante"),
                "escudo_mandante": mandante_info.get("team", {}).get("logo", ""),
                "visitante": visitante_info.get("team", {}).get("displayName", "Visitante"),
                "escudo_visitante": visitante_info.get("team", {}).get("logo", ""),
                "placar_mandante": int(mandante_info.get("score", 0)),
                "placar_visitante": int(visitante_info.get("score", 0)),
                "acrescimo_1t": None,
                "acrescimo_2t": None,
                "eventos": []
            }
            partidas_processadas.append(partida)
            
        return partidas_processadas

class TabelaManager:
    """Calcula a classificação e aplica a regra visual de rebaixamento (vermelho)."""

    @staticmethod
    def processar_rebaixamento(tabela_crua: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        total = len(tabela_crua)
        for idx, item in enumerate(tabela_crua):
            pos = idx + 1
            zona = "rebaixamento" if pos >= (total - 1) else "normal"
            item["posicao"] = pos
            item["zona"] = zona
            item["cor_destaque"] = "vermelho" if zona == "rebaixamento" else "neutro"
        return tabela_crua
