import httpx
from typing import List, Dict, Any
from config import settings

class ESPNPublicService:
    """Faz as requisições diretas na API pública da ESPN."""

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
        
        # Modo de Espera / Fallback: Se não houver jogos ao vivo na ESPN,
        # retorna a tabela com os confrontos pré-definidos para o início do campeonato.
        if not eventos_espn:
            return [
                {
                    "id_partida": "101",
                    "rodada": 1,
                    "status": "NS",
                    "status_descricao": "Agendado / Aguardando Início",
                    "data_hora": "2027-01-17T16:00:00Z",
                    "estadio": "Morumbi",
                    "mandante": "São Paulo",
                    "escudo_mandante": "https://a.espncdn.com/i/teamlogos/soccer/500/2033.png",
                    "visitante": "Corinthians",
                    "escudo_visitante": "https://a.espncdn.com/i/teamlogos/soccer/500/872.png",
                    "placar_mandante": 0,
                    "placar_visitante": 0,
                    "acrescimo_1t": None,
                    "acrescimo_2t": None,
                    "eventos": []
                },
                {
                    "id_partida": "102",
                    "rodada": 1,
                    "status": "NS",
                    "status_descricao": "Agendado / Aguardando Início",
                    "data_hora": "2027-01-17T18:30:00Z",
                    "estadio": "Allianz Parque",
                    "mandante": "Palmeiras",
                    "escudo_mandante": "https://a.espncdn.com/i/teamlogos/soccer/500/2026.png",
                    "visitante": "Santos",
                    "escudo_visitante": "https://a.espncdn.com/i/teamlogos/soccer/500/2045.png",
                    "placar_mandante": 0,
                    "placar_visitante": 0,
                    "acrescimo_1t": None,
                    "acrescimo_2t": None,
                    "eventos": []
                }
            ]

        # Caso a ESPN retorne dados reais (quando o campeonato estiver rolando)
        partidas_processadas = []
        for idx, evento in enumerate(eventos_espn):
            competicao = evento.get("competitions", [{}])[0]
            status_obj = evento.get("status", {}).get("type", {})
            status_sigla = status_obj.get("state", "pre")
            
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
    """Calcula a classificação e aplica o destaque na zona de rebaixamento."""

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
