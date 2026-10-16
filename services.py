import requests

# 1. LISTA DE TIMES EXCLUÍDOS
TIMES_EXCLUIDOS = ["Noroeste", "Velo Clube", "EC Noroeste"]

# 2. DICIONÁRIO COMPLETO COM OS 15 ESCUDOS (Dourados, PNG Transparente e Padrão)
ESCUDOS_CUSTOMIZADOS = {
    "Novorizontino": "https://i.postimg.cc/c4CRh8gm/D-NQ-NP-783305-MLB110188064885-042026-0-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-removebg-preview.png",
    "Palmeiras": "https://i.postimg.cc/c4CRh8gm/D-NQ-NP-783305-MLB110188064885-042026-0-escudo-especial-palmeiras-ouro-50x50-grande-placa-decor-removebg-preview.png",
    "Red Bull Bragantino": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "Portuguesa": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "Corinthians": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "São Paulo": "https://i.postimg.cc/nrcP0cBq/D-NQ-NP-876716-MLB110894002000-052026-F-removebg-preview.png",
    "Capivariano": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Santos": "https://i.postimg.cc/kG8B2sVc/images-removebg-preview.png",
    "Guarani": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Botafogo-SP": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Mirassol": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Primavera SP": "https://i.postimg.cc/N0JjcJc0/1000085816-removebg-preview.png",
    "Primavera": "https://i.postimg.cc/N0JjcJc0/1000085816-removebg-preview.png",
    "São Bernardo": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Ferroviária": "https://i.postimg.cc/66S3Ckt7/afe.png",
    "Juventus SP": "https://i.postimg.cc/kG8B2sVc/images-removebg-preview.png",
    "Juventus": "https://i.postimg.cc/kG8B2sVc/images-removebg-preview.png"
}

# 3. LISTA OFICIAL DOS 15 CLUBES
TIMES_SERIE_A1 = [
    "Novorizontino", "Palmeiras", "Red Bull Bragantino", "Portuguesa", "Corinthians",
    "São Paulo", "Capivariano", "Santos", "Guarani", "Botafogo-SP",
    "Mirassol", "Primavera SP", "São Bernardo", "Ferroviária", "Juventus SP"
]

def obter_escudo(nome_time):
    return ESCUDOS_CUSTOMIZADOS.get(nome_time, f"https://via.placeholder.com/150?text={nome_time}")

def get_tabela():
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
        }
    ]
    return partidas
