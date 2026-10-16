import os
import requests
from typing import Dict, Any, List

# Dicionário permanente de escudos customizados
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
    "ferroviária": "https://i.postimg.cc/66S3Ckt7/ad92fcd869cb0047d7c4af335b575762-removebg-preview.png",
    "ferroviaria": "https://i.postimg.cc/66S3Ckt7/ad92fcd869cb0047d7c4af335b575762-removebg-preview.png",
    "afe": "https://i.postimg.cc/66S3Ckt7/ad92fcd869cb0047d7c4af335b575762-removebg-preview.png",
    "capivariano": "https://i.postimg.cc/g0FcgF7T/images-1-removebg-preview.png",
    "primavera": "https://i.postimg.cc/SNt2ktnW/logo-ebook.png",
    "primavera sp": "https://i.postimg.cc/SNt2ktnW/logo-ebook.png",
    "ec primavera": "https://i.postimg.cc/SNt2ktnW/logo-ebook.png",
    "juventus": "https://i.postimg.cc/kG8B2sVc/Juventus-SP-logo.png",
    "juventus sp": "https://i.postimg.cc/kG8B2sVc/Juventus-SP-logo.png",
    "ca juventus": "https://i.postimg.cc/kG8B2sVc/Juventus-SP-logo.png",
    "clube atlético juventus": "https://i.postimg.cc/kG8B2sVc/Juventus-SP-logo.png",
    "botafogo": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "botafogo-sp": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "botafogo sp": "https://i.postimg.cc/RF9HbbhF/0x1900-000000-80-0-0-removebg-preview.png",
    "guarani": "https://i.postimg.cc/N0JjcJjc/Whats-App-Image-2023-06-19-at-10-35-15-removebg-preview.png",
    "novorizontino": "https://i.postimg.cc/FKQjSKyF/images-removebg-preview.png",
    "bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png",
    "red bull bragantino": "https://i.postimg.cc/xdJpg87w/51293636497-d1e335da5a-o-1024x698-removebg-preview.png"
}

# Lista de clubes proibidos / excluídos (Série A1 2027)
TIMES_EXCLUIDOS = {
    "ponte preta", "aa ponte preta",
    "velo clube", "ae velo clube", "velo clube sp",
    "água santa", "agua santa", "ec água santa",
    "inter de limeira", "aa inter de limeira",
    "ituano", "ituano fc",
    "noroeste", "ec noroeste"
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
    nome_norm = nome_time.strip().lower()
    for excluido in TIMES_EXCLUIDOS:
        if excluido in nome_norm:
            return False
    return True

def obter_tabela_paulistao() -> List[Dict[str, Any]]:
    """Busca a tabela de classificação oficial via ESPN API com fallback local."""
    url = "https://site.api.espn.com/apis/v2/sports/soccer/bra.camp.paulista/standings"
    
    tabela = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            children = data.get("children", [])
            if children:
                standings = children[0].get("standings", {}).get("entries", [])
                for entry in standings:
                    team_info = entry.get("team", {})
                    nome = team_info.get("displayName", "")
                    
                    if not time_permitido(nome):
                        continue
                    
                    stats = {s.get("name"): s.get("value", 0) for s in entry.get("stats", [])}
                    escudo_original = team_info.get("logos", [{}])[0].get("href", "")
                    
                    tabela.append({
                        "posicao": 0,  # Definido depois
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
    except Exception as e:
        print(f"Erro ao buscar tabela da ESPN: {e}")

    # Garante que a Ferroviária e o Juventus estejam presentes na tabela
    nomes_atuais = {t["time"].lower() for t in tabela}
    
    if not any("ferroviária" in n or "afe" in n for n in nomes_atuais):
        tabela.append({
            "posicao": 0, "time": "Ferroviária", "escudo": obter_escudo("Ferroviária"),
            "pontos": 0, "jogos": 0, "vitorias": 0, "empates": 0, "derrotas": 0,
            "gols_pro": 0, "gols_contra": 0, "saldo_gols": 0
        })
        
    if not any("juventus" in n for n in nomes_atuais):
        tabela.append({
            "posicao": 0, "time": "Juventus SP", "escudo": obter_escudo("Juventus SP"),
            "pontos": 0, "jogos": 0, "vitorias": 0, "empates": 0, "derrotas": 0,
            "gols_pro": 0, "gols_contra": 0, "saldo_gols": 0
        })

    # Ordena e reatribui as posições
    for idx, time_obj in enumerate(tabela, start=1):
        time_obj["posicao"] = idx

    return tabela if tabela else obter_tabela_fallback()

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
        
    return obter_partidas_fallback()

def obter_tabela_fallback() -> List[Dict[str, Any]]:
    times_base = [
        "São Paulo", "Corinthians", "Palmeiras", "Santos", "Portuguesa",
        "Mirassol", "São Bernardo", "Ferroviária", "Capivariano", "Primavera SP",
        "Juventus SP", "Botafogo SP", "Guarani", "Novorizontino", "Red Bull Bragantino"
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
        }
    ]
