import httpx
from typing import List, Dict, Any

class ESPNPublicService:
    # URL base da API pública da ESPN para o futebol brasileiro / estadual
    URL_API_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard"

    @classmethod
    async def obter_partidas_formatadas(cls) -> List[Dict[str, Any]]:
        """Busca os dados na ESPN, formata as informações e aplica correção nos escudos quando necessário."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(cls.URL_API_ESPN)
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                events = data.get("events", [])
                
                if not events:
                    return []

                partidas_formatadas = []
                
                for event in events:
                    competition = event.get("competitions", [{}])[0]
                    competitors = competition.get("competitors", [])
                    
                    if len(competitors) < 2:
                        continue
                        
                    # Identifica mandante e visitante
                    casa = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
                    visitante = competitors[1] if competitors[1].get("homeAway") == "away" else competitors[0]
                    
                    nome_casa = casa.get("team", {}.get("displayName", "Mandante"))
                    escudo_casa = casa.get("team", {}.get("logo", ""))
                    
                    nome_visitante = visitante.get("team", {}.get("displayName", "Visitante"))
                    escudo_visitante = visitante.get("team", {}.get("logo", ""))
                    
                    # Correção de segurança para o escudo da Portuguesa caso a ESPN traga desatualizado ou genérico
                    if "portuguesa" in nome_casa.lower():
                        escudo_casa = "https://a.espncdn.com/i/teamlogos/soccer/500/3468.png"
                    if "portuguesa" in nome_visitante.lower():
                        escudo_visitante = "https://a.espncdn.com/i/teamlogos/soccer/500/3468.png"

                    partida_info = {
                        "id": event.get("id"),
                        "data": event.get("date"),
                        "status": event.get("status", {}).get("type", {}).get("description", ""),
                        "time_casa": {
                            "nome": nome_casa,
                            "escudo": escudo_casa,
                            "placar": casa.get("score", "0")
                        },
                        "time_visitante": {
                            "nome": nome_visitante,
                            "escudo": escudo_visitante,
                            "placar": visitante.get("score", "0")
                        },
                        "estadio": competition.get("venue", {}).get("fullName", "Local a definir")
                    }
                    
                    partidas_formatadas.append(partida_info)
                    
                return partidas_formatadas
                
        except Exception as e:
            print(f"Erro ao buscar dados da ESPN: {e}")
            return []

class TabelaManager:
    @staticmethod
    def processar_rebaixamento(tabela: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gerencia a lógica de classificação e alerta de rebaixamento."""
        return tabela
