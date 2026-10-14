import httpx
from typing import List, Dict, Any

class RealFootballService:
    # Endpoint público alternativo para dados reais do Paulistão
    URL_API_REAL = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4393"
    
    # Link oficial garantido do escudo da Portuguesa de Desportos
    ESCUDO_PORTUGUESA = "https://a.espncdn.com/i/teamlogos/soccer/500/3468.png"

    @classmethod
    async def obter_partidas_formatadas(cls) -> List[Dict[str, Any]]:
        """Busca dados reais e públicos de partidas de futebol."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(cls.URL_API_REAL)
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                events = data.get("events", [])
                
                if not events:
                    return []

                partidas_formatadas = []
                
                for event in events:
                    nome_casa = event.get("strHomeTeam", "Mandante")
                    nome_visitante = event.get("strAwayTeam", "Visitante")
                    
                    escudo_casa = event.get("strHomeTeamBadge", "")
                    escudo_visitante = event.get("strAwayTeamBadge", "")
                    
                    # Correção garantida do escudo da Portuguesa
                    if "portuguesa" in nome_casa.lower():
                        escudo_casa = cls.ESCUDO_PORTUGUESA
                    if "portuguesa" in nome_visitante.lower():
                        escudo_visitante = cls.ESCUDO_PORTUGUESA

                    partida_info = {
                        "id": event.get("idEvent"),
                        "data": event.get("dateEvent"),
                        "status": event.get("strStatus", "Agendado"),
                        "time_casa": {
                            "nome": nome_casa,
                            "escudo": escudo_casa,
                            "placar": event.get("intHomeScore") or "0"
                        },
                        "time_visitante": {
                            "nome": nome_visitante,
                            "escudo": escudo_visitante,
                            "placar": event.get("intAwayScore") or "0"
                        },
                        "estadio": event.get("strVenue", "Estádio Municipal")
                    }
                    
                    partidas_formatadas.append(partida_info)
                    
                return partidas_formatadas
                
        except Exception as e:
            print(f"Erro ao buscar dados reais: {e}")
            return []

class TabelaManager:
    @staticmethod
    def processar_rebaixamento(tabela: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return tabela

class ESPNPublicService:
    @classmethod
    async def obter_partidas_formatadas(cls):
        return await RealFootballService.obter_partidas_formatadas()
