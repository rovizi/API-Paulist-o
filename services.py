import httpx
from typing import List, Dict, Any

# Dicionário oficial com os escudos do Paulistão:
# - 4 Grandes: Logos Douradas
# - Portuguesa: Logo Prateada
# - Demais clubes: Logos Padronizadas
ESCUDOS_TIMES = {
    # Os 4 Grandes (Logos Douradas)
    "são paulo": "https://i.postimg.cc/RZhBLtHd/Gemini-Generated-Image-w9fhmqw9fhmqw9fh-removebg-preview.png",
    "corinthians": "https://i.postimg.cc/9FGpggG4/Gemini-Generated-Image-dd6vlvdd6vlvdd6v-removebg-preview.png",
    "palmeiras": "https://i.postimg.cc/VkdVSxZH/D-NQ-NP-783305-MLB110188064885-042026-O-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-rem.png",
    "santos": "https://i.postimg.cc/Kc7HXvBx/fundo-2-removebg-preview.png",
    
    # Portuguesa (Logo Prateada)
    "portuguesa": "https://i.postimg.cc/MTM4n0gb/Gemini-Generated-Image-vtv2kgvtv2kgvtv2-removebg-preview.png",
    
    # Demais clubes participantes oficiais
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

# Lista dos 4 times que NÃO disputam e devem ser removidos de todo o sistema
TIMES_REMOVIDOS = ["ponte preta", "velo clube", "água santa", "inter de limeira"]

class ESPNPublicService:
    URL_API_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.paulista/scoreboard"

    @classmethod
    def deve_remover_time(cls, nome_time: str) -> bool:
        """Verifica se o time está na lista de removidos."""
        if not nome_time:
            return False
        nome_clean = nome_time.lower().strip()
        return any(removido in nome_clean for removido in TIMES_REMOVIDOS)

    @classmethod
    def buscar_escudo_customizado(cls, nome_time: str, escudo_original: str = "") -> str:
        """Busca o escudo customizado (dourados para os grandes, prateado para a Portuguesa, padrão para os demais)."""
        if not nome_time:
            return escudo_original
            
        nome_clean = nome_time.lower().strip()
        for chave, url_escudo in ESCUDOS_TIMES.items():
            if chave in nome_clean:
                return url_escudo
        return escudo_original

    @classmethod
    async def obter_partidas_formatadas(cls, rodada: int = 1) -> List[Dict[str, Any]]:
        """Busca confrontos em tempo real, filtra os removidos e define status 'A confirmar'."""
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
                    nome_visitante = visitante.get("team", {}).get("displayName", "Visitante")
                    
                    # Filtra e ignora partidas que envolvam os times removidos
                    if cls.deve_remover_time(nome_casa) or cls.deve_remover_time(nome_visitante):
                        continue

                    escudo_casa_espn = casa.get("team", {}).get("logo", "")
                    escudo_visitante_espn = visitante.get("team", {}).get("logo", "")
                    
                    escudo_casa = cls.buscar_escudo_customizado(nome_casa, escudo_casa_espn)
                    escudo_visitante = cls.buscar_escudo_customizado(nome_visitante, escudo_visitante_espn)

                    partida_info = {
                        "id_partida": str(event.get("id", f"espn-{index}")),
                        "rodada": rodada,
                        "status": "pre",
                        "status_descricao": "A confirmar",
                        "data_hora": event.get("date", ""),
                        "estadio": competition.get("venue", {}).get("fullName", "Local a definir"),
                        "mandante": nome_casa,
                        "escudo_mandante": escudo_casa,
                        "visitante": nome_visitante,
                        "escudo_visitante": escudo_visitante,
                        "placar_mandante": 0,
                        "placar_visitante": 0,
                        "acrescimo_1t": None,
                        "acrescimo_2t": None,
                        "eventos": []
                    }
                    
                    partidas_formatadas.append(partida_info)
                    
                return partidas_formatadas
                
        except Exception as e:
            print(f"Erro ao buscar dados da ESPN: {e}")
            return []

class TabelaManager:
    CAMPEONATO_INICIADO = False

    @classmethod
    def formatar_tabela_classificacao(cls, tabela_raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formata a tabela:
        1. Remove os 4 times banidos.
        2. Aplica as logos douradas e prateada.
        3. Mantém a pontuação zerada até o início do campeonato.
        """
        tabela_formatada = []
        posicao_real = 1

        for item in tabela_raw:
            nome_time = item.get("time", item.get("nome", ""))
            
            if ESPNPublicService.deve_remover_time(nome_time):
                continue
            
            escudo = ESPNPublicService.buscar_escudo_customizado(nome_time, item.get("escudo", ""))

            if not cls.CAMPEONATO_INICIADO:
                pontos, jogos, vitorias, empates, derrotas = 0, 0, 0, 0, 0
                gols_pro, gols_contra, saldo_gols = 0, 0, 0
            else:
                pontos = item.get("pontos", 0)
                jogos = item.get("jogos", 0)
                vitorias = item.get("vitorias", 0)
                empates = item.get("empates", 0)
                derrotas = item.get("derrotas", 0)
                gols_pro = item.get("gols_pro", 0)
                gols_contra = item.get("gols_contra", 0)
                saldo_gols = item.get("saldo_gols", 0)

            tabela_formatada.append({
                "posicao": posicao_real,
                "time": nome_time,
                "escudo": escudo,
                "pontos": pontos,
                "jogos": jogos,
                "vitorias": vitorias,
                "empates": empates,
                "derrotas": derrotas,
                "gols_pro": gols_pro,
                "gols_contra": gols_contra,
                "saldo_gols": saldo_gols
            })
            posicao_real += 1

        return tabela_formatada
