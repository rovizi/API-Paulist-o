import httpx
from typing import List, Dict, Any

# Dicionário oficial com os escudos do Paulistão - Atualizado e Padronizado
ESCUDOS_TIMES = {
    "são paulo": "https://i.postimg.cc/RZhBLtHd/Gemini-Generated-Image-w9fhmqw9fhmqw9fh-removebg-preview.png",
    "corinthians": "https://i.postimg.cc/9FGpggG4/Gemini-Generated-Image-dd6vlvdd6vlvdd6v-removebg-preview.png",
    "mirassol": "https://i.postimg.cc/WbH2KSTj/59cde20b84400f9798e8e3b6478ea8c9-removebg-preview.png",
    "portuguesa": "https://i.postimg.cc/MTM4n0gb/Gemini-Generated-Image-vtv2kgvtv2kgvtv2-removebg-preview.png",
    "são bernardo": "https://i.postimg.cc/G3NLgqc4/logo-removebg-preview-(1).png",
    
    # Demais clubes mantidos com as URLs padrão anteriores
    "santos": "https://i.postimg.cc/Kc7HXvBx/fundo-2-removebg-preview.png",
    "palmeiras": "https://i.postimg.cc/VkdVSxZH/D-NQ-NP-783305-MLB110188064885-042026-O-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-rem.png",
    "juventus": "https://i.postimg.cc/L4fr9FYy/images.jpg",
    "ferroviária": "https://i.postimg.cc/rp2TTGMP/ad92fcd869cb0047d7c4af335b575762.jpg",
    "capivariano": "https://i.postimg.cc/g0FcgF7T/images-1-removebg-preview.png",
    "primavera": "https://i.postimg.cc/rwmcgygY/fa3d503d6e230d22e64c62ae8db51597-c6bf0fb7a0f6ee112f17652856885912-1024-1024-removebg-preview.png",
    "botafogo": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "noroeste": "https://i.postimg.cc/9Xwvm8Qz/0x1900-000000-80-0-0-removebg-preview.png",
    "guarani": "https://i.postimg.cc/N0JjcJjc/Whats-App-Image-2023-06-19-at-10-35-15-removebg-preview.png",
    "novorizontino": "https://i.postimg.cc/FKQjSKyF/images-removebg-preview.png",
    "bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png"
}

class ESPNPublicService:
    URL_API_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.paulista/scoreboard"

    @classmethod
    def buscar_escudo_customizado(cls, nome_time: str, escudo_original: str = "") -> str:
        """Busca o escudo customizado com base no nome do time."""
        if not nome_time:
            return escudo_original
            
        nome_clean = nome_time.lower().strip()
        for chave, url_escudo in ESCUDOS_TIMES.items():
            if chave in nome_clean:
                return url_escudo
        return escudo_original

    @classmethod
    async def obter_partidas_formatadas(cls, rodada: int = 1) -> List[Dict[str, Any]]:
        """Busca confrontos na ESPN e os formata exatamente de acordo com o PartidaResponse."""
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
                
                for index, event in enumerate(events, start=1):
                    competition = event.get("competitions", [{}])[0]
                    competitors = competition.get("competitors", [])
                    
                    if len(competitors) < 2:
                        continue
                        
                    casa = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
                    visitante = competitors[1] if competitors[1].get("homeAway") == "away" else competitors[0]
                    
                    nome_casa = casa.get("team", {}).get("displayName", "Mandante")
                    escudo_casa_espn = casa.get("team", {}).get("logo", "")
                    
                    nome_visitante = visitante.get("team", {}).get("displayName", "Visitante")
                    escudo_visitante_espn = visitante.get("team", {}).get("logo", "")
                    
                    escudo_casa = cls.buscar_escudo_customizado(nome_casa, escudo_casa_espn)
                    escudo_visitante = cls.buscar_escudo_customizado(nome_visitante, escudo_visitante_espn)

                    partida_info = {
                        "id_partida": str(event.get("id", f"espn-{index}")),
                        "rodada": rodada,
                        "status": event.get("status", {}).get("type", {}).get("state", "pre"),
                        "status_descricao": event.get("status", {}).get("type", {}).get("description", "Agendado"),
                        "data_hora": event.get("date", ""),
                        "estadio": competition.get("venue", {}).get("fullName", "Local a definir"),
                        "mandante": nome_casa,
                        "escudo_mandante": escudo_casa,
                        "visitante": nome_visitante,
                        "escudo_visitante": escudo_visitante,
                        "placar_mandante": int(casa.get("score", 0)) if casa.get("score") else 0,
                        "placar_visitante": int(visitante.get("score", 0)) if visitante.get("score") else 0,
                        "acrescimo_1t": None,
                        "acrescimo_2t": None,
                        "eventos": []
                    }
                    
                    partidas_formatadas.append(partida_info)
                    
                return partidas_formatadas
                
        except Exception as e:
            print(f"Erro ao buscar dados da ESPN: {e}")
            return []

    @classmethod
    async def obter_partidas_teste(cls, rodada: int = 1) -> List[Dict[str, Any]]:
        """Gera 8 confrontos de teste validando rigorosamente o modelo PartidaResponse."""
        confrontos_mock = [
            ("Santos", "Corinthians", "Vila Belmiro"),
            ("São Paulo", "Portuguesa", "MorumBIS"),
            ("Mirassol", "Palmeiras", "José Maria de Campos Maia"),
            ("Red Bull Bragantino", "Botafogo-SP", "Nabi Abi Chedid"),
            ("Ferroviária", "Novorizontino", "Fonte Luminosa"),
            ("São Bernardo", "Capivariano", "Primeiro de Maio"),
            ("Noroeste", "Primavera", "Alfredo de Castilho"),
            ("Juventus", "Guarani", "Rua Javari")
        ]

        partidas_teste = []
        for index, (mandante, visitante, estadio) in enumerate(confrontos_mock, start=1):
            partidas_teste.append({
                "id_partida": f"teste-{index}",
                "rodada": rodada,
                "status": "NS",
                "status_descricao": "Agendado (Simulação)",
                "data_hora": "2027-01-20T19:30:00Z",
                "estadio": estadio,
                "mandante": mandante,
                "escudo_mandante": cls.buscar_escudo_customizado(mandante),
                "visitante": visitante,
                "escudo_visitante": cls.buscar_escudo_customizado(visitante),
                "placar_mandante": 0,
                "placar_visitante": 0,
                "acrescimo_1t": None,
                "acrescimo_2t": None,
                "eventos": []
            })

        return partidas_teste

class TabelaManager:
    @staticmethod
    def processar_rebaixamento(tabela: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return tabela
