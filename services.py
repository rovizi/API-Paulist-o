import requests

# 1. LISTA DE TIMES EXCLUÍDOS (Não entram na Série A1 do Paulistão)
TIMES_EXCLUIDOS = ["Noroeste", "Velo Clube", "EC Noroeste"]

# 2. DICIONÁRIO COMPLETO DE ESCUDOS CUSTOMIZADOS
# Mantém todas as suas imagens PNG transparentes e versões especiais (como o Novorizontino Ouro)
ESCUDOS_CUSTOMIZADOS = {
    "Novorizontino": "https://i.postimg.cc/c4CRh8gm/D-NQ-NP-783305-MLB110188064885-042026-0-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-removebg-preview.png",
    "Portuguesa": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "Ferroviária": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Primavera SP": "https://i.postimg.cc/N0JjcJc0/1000085816-removebg-preview.png",
    "Primavera": "https://i.postimg.cc/N0JjcJc0/1000085816-removebg-preview.png",
    "Juventus SP": "https://i.postimg.cc/kG8B2sVc/images-removebg-preview.png",
    "Juventus": "https://i.postimg.cc/kG8B2sVc/images-removebg-preview.png",
}

# 3. LISTA OFICIAL DOS 15 CLUBES DA SÉRIE A1
TIMES_SERIE_A1 = [
    "Novorizontino", "Palmeiras", "Red Bull Bragantino", "Portuguesa", "Corinthians",
    "São Paulo", "Capivariano", "Santos", "Guarani", "Botafogo-SP",
    "Mirassol", "Primavera SP", "São Bernardo", "Ferroviária", "Juventus SP"
]

def obter_escudo(nome_time):
    """Retorna o escudo customizado ou gera um fallback"""
    return ESCUDOS_CUSTOMIZADOS.get(nome_time, f"https://via.placeholder.com/150?text={nome_time}")

def get_tabela():
    """Retorna a tabela do Paulistão com pontuações zeradas e mantendo os escudos oficiais"""
    tabela_zerada = []

    for posicao, time_nome in enumerate(TIMES_SERIE_A1, start=1):
        tabela_zerada.append({
            "posicao": posicao,
            "time": time_nome,
            "escudo": obter_escudo(time_nome),
            "pontos": 0,
            "jogos": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "gols_pro": 0,
            "gols_contra": 0,
            "saldo_gols": 0
        })

    return tabela_zerada

def get_partidas():
    """Retorna a lista inicial de confrontos pré-temporada zerada"""
    partidas = [
        {
            "data": "2027-01-15T19:00:00Z",
            "status": "NS",
            "estadio": "A definir",
            "mandante": "Santos",
            "escudo_mandante": obter_escudo("Santos"),
            "placar_mandante": 0,
            "visitante": "Novorizontino",
            "escudo_visitante": obter_escudo("Novorizontino"),
            "placar_visitante": 0
        },
        {
            "data": "2027-01-15T21:30:00Z",
            "status": "NS",
            "estadio": "A definir",
            "mandante": "Palmeiras",
            "escudo_mandante": obter_escudo("Palmeiras"),
            "placar_mandante": 0,
            "visitante": "Red Bull Bragantino",
            "escudo_visitante": obter_escudo("Red Bull Bragantino"),
            "placar_visitante": 0
        }
    ]
    return partidas
