
import httpx
from typing import List, Dict, Any

# Dicionário oficial com os escudos customizados (Dourados/Prata + Padrões)
ESCUDOS_TIMES = {
    # Os 4 Grandes + Portuguesa (Logos Douradas)
    "são paulo": "https://i.postimg.cc/hjCJQprP/Gemini-Generated-Image-n6n9n7n6n9n7n6n9-removebg-preview.png",
    "corinthians": "https://i.postimg.cc/bNpMwg5j/D-NQ-NP-891136-MLB101696524221-122025-O-placa-painel-em-pvc-50x50-escudo-corinthians-gold-timao.webp",
    "palmeiras": "https://i.postimg.cc/c4CRh8gm/D-NQ-NP-783305-MLB110188064885-042026-O-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-rem.png",
    "santos": "https://i.postimg.cc/qMJbTRtN/D-NQ-NP-839454-MLB82114445831-012025-O-removebg-preview.png",
    "portuguesa": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    
    # Demais clubes participantes oficiais da Série A
    "mirassol": "https://i.postimg.cc/WbH2KSTj/59cde20b84400f9798e8e3b6478ea8c9-removebg-preview.png",
    "são bernardo": "https://i.postimg.cc/G3NLgqc4/logo-removebg-preview-(1).png",
    "ferroviária": "https://i.postimg.cc/rp2TTGMP/ad92fcd869cb0047d7c4af335b575762.jpg",
    "capivariano": "https://i.postimg.cc/g0FcgF7T/images-1-removebg-preview.png",
    "primavera": "https://i.postimg.cc/rwmcgygY/fa3d503d6e230d22e64c62ae8db51597-c6bf0fb7a0f6ee112f17652856885912-1024-1024-removebg-preview.png",
    "botafogo": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "noroeste": "https://i.postimg.cc/9Xwvm8Qz/0x1900-000000-80-0-0-removebg-preview.png",
    "guarani": "https://i.postimg.cc/N0JjcJjc/Whats-App-Image-2023-06-19-at-10-35-15-removebg-preview.png",
    "novorizontino": "https://i.postimg.cc/FKQjSKyF/images-removebg-preview.png",
    "bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png"
}

# Lista restrita de times removidos da Série A (Incluindo o Ituano)
TIMES_REMOVIDOS = ["ponte preta", "velo clube", "água santa", "inter de limeira", "ituano"]

class ESPNPublicService:
    URL_API_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.paulista/scoreboard"

    @classmethod
    def deve_remover_time(cls, nome_time: str) -> bool:
        """Verifica se o time está na lista de banidos/removidos."""
        if not nome_time:
            return False
        nome_clean = nome_time.lower().strip()
        return any(removido in nome_clean for removido in TIMES_REMOVIDOS)

    @classmethod
    def buscar_escudo_customizado(cls, nome_time: str, escudo_original: str = "") -> str:
        """Busca o escudo customizado (dourado/prata) ou mantém o original se não estiver na lista."""
        if not nome_time:
            return escudo_original
        nome_clean = nome_time.lower().strip()
        for chave, url_escudo in ESCUDOS_TIMES.items():
            if chave in nome_clean:
                return url_escudo
        return escudo_original

    @classmethod
    async def obter_partidas_formatadas(cls, rodada: int = 1) -> List[Dict[str, Any]]:
        """
        Tenta buscar dados reais da ESPN. 
        Se o campeonato estiver inativo (fora de temporada), retorna o fallback com 'A confirmar' e escudos dourados.
        Se estiver ativo, puxa os confrontos reais aplicando os escudos dourados e status ao vivo.
        """
        partidas_formatadas = []
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(cls.URL_API_ESPN)
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    for index, event in enumerate(events, start=1):
                        competition = event.get("competitions", [{}])[0]
                        competitors = competition.get("competitors", [])
                        
                        if len(competitors) < 2:
                            continue
                            
                        casa = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
                        visitante = competitors[1] if competitors[1].get("homeAway") == "away" else competitors[0]
                        
                        nome_casa = casa.get("team", {}).get("displayName", "Mandante")
                        nome_visitante = visitante.get("team", {}).get("displayName", "Visitante")
                        
                        # Filtra e ignora times removidos
                        if cls.deve_remover_time(nome_casa) or cls.deve_remover_time(nome_visitante):
                            continue

                        # Injeção dinâmica do escudo dourado sobre o escudo da ESPN
                        escudo_casa_espn = casa.get("team", {}).get("logo", "")
                        escudo_visitante_espn = visitante.get("team", {}).get("logo", "")
                        
                        escudo_casa = cls.buscar_escudo_customizado(nome_casa, escudo_casa_espn)
                        escudo_visitante = cls.buscar_escudo_customizado(nome_visitante, escudo_visitante_espn)

                        status_type = event.get("status", {}).get("type", {})
                        status_state = status_type.get("state", "pre")
                        status_desc = status_type.get("shortDetail", "A confirmar")

                        partida_info = {
                            "id_partida": str(event.get("id", f"espn-{index}")),
                            "rodada": rodada,
                            "status": status_state,
                            "status_descricao": status_desc,
                            "data_hora": event.get("date", ""),
                            "estadio": competition.get("venue", {}).get("fullName", "Local a definir"),
                            "mandante": nome_casa,
                            "escudo_mandante": escudo_casa,
                            "visitante": nome_visitante,
                            "escudo_visitante": escudo_visitante,
                            "placar_mandante": int(casa.get("score", 0)),
                            "placar_visitante": int(visitante.get("score", 0)),
                            "acrescimo_1t": None,
                            "acrescimo_2t": None,
                            "eventos": []
                        }
                        
                        partidas_formatadas.append(partida_info)
                        
        except Exception as e:
            print(f"Erro ao buscar ESPN: {e}")

        # Se não houver dados ativos na ESPN, exibe o fallback com "A confirmar" e escudos dourados
        if not partidas_formatadas:
            return cls._gerar_partidas_fallback(rodada)

        return partidas_formatadas

    @classmethod
    def _gerar_partidas_fallback(cls, rodada: int) -> List[Dict[str, Any]]:
        """Gera partidas padrão com status 'A confirmar' e escudos dourados enquanto o campeonato não inicia."""
        return [
            {
                "id_partida": "paulista-2027-1",
                "rodada": rodada,
                "status": "pre",
                "status_descricao": "A confirmar",
                "data_hora": "2027-01-15T20:00:00Z",
                "estadio": "Morumbi",
                "mandante": "São Paulo",
                "escudo_mandante": ESCUDOS_TIMES["são paulo"],
                "visitante": "Corinthians",
                "escudo_visitante": ESCUDOS_TIMES["corinthians"],
                "placar_mandante": 0,
                "placar_visitante": 0,
                "acrescimo_1t": None,
                "acrescimo_2t": None,
                "eventos": []
            },
            {
                "id_partida": "paulista-2027-2",
                "rodada": rodada,
                "status": "pre",
                "status_descricao": "A confirmar",
                "data_hora": "2027-01-15T21:30:00Z",
                "estadio": "Allianz Parque",
                "mandante": "Palmeiras",
                "escudo_mandante": ESCUDOS_TIMES["palmeiras"],
                "visitante": "Santos",
                "escudo_visitante": ESCUDOS_TIMES["santos"],
                "placar_mandante": 0,
                "placar_visitante": 0,
                "acrescimo_1t": None,
                "acrescimo_2t": None,
                "eventos": []
            },
            {
                "id_partida": "paulista-2027-3",
                "rodada": rodada,
                "status": "pre",
                "status_descricao": "A confirmar",
                "data_hora": "2027-01-16T18:00:00Z",
                "estadio": "Canindé",
                "mandante": "Portuguesa",
                "escudo_mandante": ESCUDOS_TIMES["portuguesa"],
                "visitante": "Guarani",
                "escudo_visitante": ESCUDOS_TIMES["guarani"],
                "placar_mandante": 0,
                "placar_visitante": 0,
                "acrescimo_1t": None,
                "acrescimo_2t": None,
                "eventos": []
            }
        ]

class TabelaManager:
    CAMPEONATO_INICIADO = False

    @classmethod
    def formatar_tabela_classificacao(cls, tabela_raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera a tabela completa com escudos customizados e estatísticas zeradas."""
        tabela_formatada = []
        posicao = 1

        for nome_time, url_escudo in ESCUDOS_TIMES.items():
            tabela_formatada.append({
                "posicao": posicao,
                "time": nome_time.title(),
                "escudo": url_escudo,
                "pontos": 0,
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_pro": 0,
                "gols_contra": 0,
                "saldo_gols": 0
            })
            posicao += 1

        return tabela_formatada
