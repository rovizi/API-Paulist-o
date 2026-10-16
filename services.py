
iimport os
import requests
from typing import Dict, Any, List

# Dicionário permanente de escudos customizados (Dourados para o Big Four, Silver para Portuguesa e URLs diretas)
ESCUDOS_TIMES: Dict[str, str] = {
    "são paulo": "https://i.postimg.cc/hjCJQprP/Gemini-Generated-Image-n6n9n7n6n9n7n6n9-removebg-preview.png",
    "sao paulo": "https://i.postimg.cc/hjCJQprP/Gemini-Generated-Image-n6n9n7n6n9n7n6n9-removebg-preview.png",
    "corinthians": "https://i.postimg.cc/FHtrTbMR/Gemini-Generated-Image-j1dxhqj1dxhqj1dx-removebg-preview.png",
    "palmeiras": "https://i.postimg.cc/c4CRh8gm/D-NQ-NP-783305-MLB110188064885-042026-O-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-rem.png",
    "santos": "https://i.postimg.cc/qMJbTRtN/D-NQ-NP-839454-MLB82114445831-012025-O-removebg-preview.png",
    "portuguesa": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "mirassol": "https://i.postimg.cc/WbH2KSTj/59cde20b84400f9798e8e3b6478ea8c9-removebg-preview.png",
    "são bernardo": "https://i.postimg.cc/G3NLgqc4/logo-removebg-preview-(1).png",
    "sao bernardo": "https://i.postimg.cc/G3NLgqc4/logo-removebg-preview-(1).png",
    "ferroviária": "https://i.postimg.cc/rp2TTGMP/ad92fcd869cb0047d7c4af335b575762.jpg",
    "ferroviaria": "https://i.postimg.cc/rp2TTGMP/ad92fcd869cb0047d7c4af335b575762.jpg",
    "capivariano": "https://i.postimg.cc/g0FcgF7T/images-1-removebg-preview.png",
    "primavera": "https://i.postimg.cc/rwmcgygY/fa3d503d6e230d22e64c62ae8db51597-c6bf0fb7a0f6ee112f17652856885912-1024-1024-removebg-preview.png",
    "botafogo": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "botafogo-sp": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "noroeste": "https://i.postimg.cc/9Xwvm8Qz/0x1900-000000-80-0-0-removebg-preview.png",
    "guarani": "https://i.postimg.cc/N0JjcJjc/Whats-App-Image-2023-06-19-at-10-35-15-removebg-preview.png",
    "novorizontino": "https://i.postimg.cc/FKQjSKyF/images-removebg-preview.png",
    "bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png",
    "red bull bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png"
}

# Lista de clubes proibidos / excluídos (Série A1 2027)
TIMES_EXCLUIDOS = {
    "ponte preta", 
    "velo clube", 
    "água santa", 
    "agua santa", 
    "inter de limeira", 
    "ituano"
}

def obter_escudo(nome_time: str, escudo_padrao: str = "") -> str:
    """Retorna o escudo customizado se existir; caso contrário, mantém o padrão enviado."""
    if not nome_time:
        return escudo_padrao
    nome_norm = nome_time.strip().lower()
    return ESCUDOS_TIMES.get(nome_norm, escudo_padrao)

def time_permitido(nome_time: str) -> bool:
    """Valida se o time não está na lista de excluídos."""
    if not nome_time:
        return True
    return nome_time.strip().lower() not in TIMES_EXCLUIDOS

def obter_tabela_paulistao() -> List[Dict[str, Any]]:
    """Busca a tabela de classificação oficial via ESPN API com fallback local."""
    url = "https://site.api.espn.com/apis/v2/sports/soccer/bra.camp.paulista/standings"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tabela = []
            
            # Navega na estrutura do JSON da ESPN
            children = data.get("children", [])
            if children:
                standings = children[0].get("standings", {}).get("entries", [])
                for idx, entry in enumerate(standings, start=1):
                    team_info = entry.get("team", {})
                    nome = team_info.get("displayName", "")
                    
                    if not time_permitido(nome):
                        continue
                    
                    # Extrai estatísticas se disponíveis
                    stats = {s.get("name"): s.get("value", 0) for s in entry.get("stats", [])}
                    
                    escudo_original = team_info.get("logos", [{}])[0].get("href", "")
                    
                    tabela.append({
                        "posicao": len(tabela) + 1,
                        "time": nome,
                        "escudo": obter_escudo(nome, escudo_original),
                        "pontos": int(stats.get("points", 0)),
                        "jogos": int(stats.get("gamesPlayed", 0)),
                        "vitorias": int(stats.get("wins", 0)),
                        "empates": int(stats.get("ties", 0)),
                        "derrotas": int(stats.get("losses", 0)),
                        "gols_pro": int(stats.get("pointsFor", 0)),
                        "gols_contra": int(stats.get("pointsAgainst", 0)),
                        "saldo_gols": int(stats.get("pointDifferential", 0))
                    })
                
                if tabela:
                    return tabela
    except Exception as e:
        print(f"Erro ao buscar tabela da ESPN: {e}")
        
    # Fallback caso a ESPN esteja fora do ar ou sem dados
    return obter_tabela_fallback()

def obter_partidas_paulistao() -> List[Dict[str, Any]]:
    """Busca as partidas oficiais via ESPN API com fallback local."""
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.camp.paulista/scoreboard"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            partidas = []
            
            for event in events:
                competition = event.get("competitions", [{}])[0]
                competitors = competition.get("competitors", [])
                
                if len(competitors) < 2:
                    continue
                
                mandante_info = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
                visitante_info = competitors[1] if competitors[0].get("homeAway") == "home" else competitors[0]
                
                nome_mandante = mandante_info.get("team", {}).get("displayName", "")
                nome_visitante = visitante_info.get("team", {}).get("displayName", "")
                
                if not time_permitido(nome_mandante) or not time_permitido(nome_visitante):
                    continue
                
                escudo_m_orig = mandante_info.get("team", {}).get("logo", "")
                escudo_v_orig = visitante_info.get("team", {}).get("logo", "")
                
                partidas.append({
                    "id": event.get("id"),
                    "data": event.get("date"),
                    "status": event.get("status", {}).get("type", {}).get("shortDetail", "A confirmar"),
                    "estadio": competition.get("venue", {}).get("fullName", "A definir"),
                    "mandante": nome_mandante,
                    "escudo_mandante": obter_escudo(nome_mandante, escudo_m_orig),
                    "placar_mandante": mandante_info.get("score"),
                    "visitante": nome_visitante,
                    "escudo_visitante": obter_escudo(nome_visitante, escudo_v_orig),
                    "placar_visitante": visitante_info.get("score")
                })
                
            if partidas:
                return partidas
    except Exception as e:
        print(f"Erro ao buscar partidas da ESPN: {e}")
        
    # Fallback de partidas
    return obter_partidas_fallback()

def obter_tabela_fallback() -> List[Dict[str, Any]]:
    """Tabela padrão base para o início do campeonato."""
    times_base = [
        "São Paulo", "Corinthians", "Palmeiras", "Santos", "Portuguesa",
        "Mirassol", "São Bernardo", "Ferroviária", "Capivariano", "Primavera",
        "Botafogo", "Noroeste", "Guarani", "Novorizontino", "Bragantino"
    ]
    
    tabela = []
    for idx, time in enumerate(times_base, start=1):
        tabela.append({
            "posicao": idx,
            "time": time,
            "escudo": obter_escudo(time),
            "pontos": 0,
            "jogos": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "gols_pro": 0,
            "gols_contra": 0,
            "saldo_gols": 0
        })
    return tabela

def obter_partidas_fallback() -> List[Dict[str, Any]]:
    """Partidas modelo para quando a tabela de jogos ainda não tiver iniciado na ESPN."""
    return [
        {
            "id": "f1",
            "data": "2027-01-17T16:00:00Z",
            "status": "A confirmar",
            "estadio": "Morumbi",
            "mandante": "São Paulo",
            "escudo_mandante": obter_escudo("São Paulo"),
            "placar_mandante": None,
            "visitante": "Corinthians",
            "escudo_visitante": obter_escudo("Corinthians"),
            "placar_visitante": None
        },
        {
            "id": "f2",
            "data": "2027-01-17T18:30:00Z",
            "status": "A confirmar",
            "estadio": "Canindé",
            "mandante": "Portuguesa",
            "escudo_mandante": obter_escudo("Portuguesa"),
            "placar_mandante": None,
            "visitante": "Guarani",
            "escudo_visitante": obter_escudo("Guarani"),
            "placar_visitante": None
        }
    ]
