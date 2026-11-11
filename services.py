# -*- coding: utf-8 -*-

"""
services.py - Fonte da verdade para dados do Paulistão 2027.
Gerencia os escudos padronizados dos 16 clubes da Série A1.
"""

ESCUDOS_CUSTOMIZADOS = {
    "Santos": "https://i.postimg.cc/qRfYVfhX/Santos-Logo.png",
    "Corinthians": "https://i.postimg.cc/vBzvPCWY/Corinthians-logo-escudo.png",
    "Palmeiras": "https://i.postimg.cc/nVXkKSXj/palmeiras.png",
    "São Paulo": "https://i.postimg.cc/tgLgKgNN/Sao-Paulo-Futebol-Clube.png",
    "Portuguesa": "https://i.postimg.cc/pLmRPHTG/portuguesa-logo-png-seeklogo-110983.png",
    "Red Bull Bragantino": "https://i.postimg.cc/VvZphJjW/Red-Bull-Bragantino.png",
    "Guarani": "https://i.postimg.cc/mDJ63vRY/Guarani-Futebol-Clube-logo-svg.webp",
    "Botafogo-SP": "https://i.postimg.cc/W4tn955w/png-clipart-botafogo-futebol-clube-botafogo-de-futebol-e-regatas-campeonato-brasileiro-serie-c-espor.png",
    "Mirassol": "https://i.postimg.cc/kXfKkx6L/Mirassol-Futebol-Clube-logo-(3-stars).png",
    "São Bernardo": "https://i.postimg.cc/ZYF3yY3X/Gemini-Generated-Image-16lgop16lgop16lg.png",
    "Primavera": "https://i.postimg.cc/L5yQRNNG/logo-ebook.png",
    "Capivariano": "https://i.postimg.cc/nL84knQn/capivariano.png",
    "Novorizontino": "https://i.postimg.cc/tJLJj4bZ/images-removebg-preview.png",
    "Ferroviária": "https://i.postimg.cc/66S3Ckt7/ad92fcd869cb0047d7c4af335b575762-removebg-preview.png",
    "Noroeste": "https://i.postimg.cc/L8PCRCtM/9500b1cc3476659e93ed698e386b2a95-removebg-preview.png",
    "Juventus": "https://i.postimg.cc/T1ySbRDP/ae184f0d31dcb85851aaab1fd2432e40.png"
}

def obter_escudo_clube(nome_clube: str) -> str:
    return ESCUDOS_CUSTOMIZADOS.get(nome_clube, "")

def zerar_estatisticas_clube(nome_clube: str) -> dict:
    return {
        "clube": nome_clube,
        "escudo": obter_escudo_clube(nome_clube),
        "pontos": 0,
        "jogos": 0,
        "vitorias": 0,
        "empates": 0,
        "derrotas": 0,
        "gols_pro": 0,
        "gols_contra": 0,
        "saldo_gols": 0
    }

def obter_tabela_paulistao() -> list:
    return [zerar_estatisticas_clube(clube) for clube in ESCUDOS_CUSTOMIZADOS.keys()]

def obter_partidas_paulistao() -> list:
    confrontos_iniciais = [
        # SÃO PAULO
        {"mandante": "São Paulo", "visitante": "Santos", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Palmeiras", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Corinthians", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Novorizontino", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Portuguesa", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Botafogo-SP", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "Mirassol", "placar": "0 x 0"},
        {"mandante": "São Paulo", "visitante": "São Bernardo", "placar": "0 x 0"},
        
        # SANTOS
        {"mandante": "Santos", "visitante": "Palmeiras", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Corinthians", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Portuguesa", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Red Bull Bragantino", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Mirassol", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Guarani", "placar": "0 x 0"},
        {"mandante": "Santos", "visitante": "Juventus", "placar": "0 x 0"},

        # PALMEIRAS
        {"mandante": "Palmeiras", "visitante": "Corinthians", "placar": "0 x 0"},
        {"mandante": "Palmeiras", "visitante": "Red Bull Bragantino", "placar": "0 x 0"},
        {"mandante": "Palmeiras", "visitante": "Capivariano", "placar": "0 x 0"},
        {"mandante": "Palmeiras", "visitante": "Guarani", "placar": "0 x 0"},
        {"mandante": "Palmeiras", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Palmeiras", "visitante": "Ferroviária", "placar": "0 x 0"},

        # CORINTHIANS
        {"mandante": "Corinthians", "visitante": "Novorizontino", "placar": "0 x 0"},
        {"mandante": "Corinthians", "visitante": "Capivariano", "placar": "0 x 0"},
        {"mandante": "Corinthians", "visitante": "Botafogo-SP", "placar": "0 x 0"},
        {"mandante": "Corinthians", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Corinthians", "visitante": "Noroeste", "placar": "0 x 0"},

        # NOVORIZONTINO
        {"mandante": "Novorizontino", "visitante": "Portuguesa", "placar": "0 x 0"},
        {"mandante": "Novorizontino", "visitante": "Red Bull Bragantino", "placar": "0 x 0"},
        {"mandante": "Novorizontino", "visitante": "Capivariano", "placar": "0 x 0"},
        {"mandante": "Novorizontino", "visitante": "Botafogo-SP", "placar": "0 x 0"},
        {"mandante": "Novorizontino", "visitante": "São Bernardo", "placar": "0 x 0"},
        {"mandante": "Novorizontino", "visitante": "Juventus", "placar": "0 x 0"},

        # PORTUGUESA
        {"mandante": "Portuguesa", "visitante": "Red Bull Bragantino", "placar": "0 x 0"},
        {"mandante": "Portuguesa", "visitante": "Capivariano", "placar": "0 x 0"},
        {"mandante": "Portuguesa", "visitante": "Mirassol", "placar": "0 x 0"},
        {"mandante": "Portuguesa", "visitante": "Juventus", "placar": "0 x 0"},
        {"mandante": "Portuguesa", "visitante": "Ferroviária", "placar": "0 x 0"},

        # RED BULL BRAGANTINO
        {"mandante": "Red Bull Bragantino", "visitante": "Capivariano", "placar": "0 x 0"},
        {"mandante": "Red Bull Bragantino", "visitante": "Guarani", "placar": "0 x 0"},
        {"mandante": "Red Bull Bragantino", "visitante": "Ferroviária", "placar": "0 x 0"},
        {"mandante": "Red Bull Bragantino", "visitante": "Noroeste", "placar": "0 x 0"},

        # CAPIVARIANO
        {"mandante": "Capivariano", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Capivariano", "visitante": "São Bernardo", "placar": "0 x 0"},
        {"mandante": "Capivariano", "visitante": "Noroeste", "placar": "0 x 0"},

        # BOTAFOGO-SP
        {"mandante": "Botafogo-SP", "visitante": "Mirassol", "placar": "0 x 0"},
        {"mandante": "Botafogo-SP", "visitante": "Guarani", "placar": "0 x 0"},
        {"mandante": "Botafogo-SP", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Botafogo-SP", "visitante": "São Bernardo", "placar": "0 x 0"},
        {"mandante": "Botafogo-SP", "visitante": "Juventus", "placar": "0 x 0"},

        # MIRASSOL
        {"mandante": "Mirassol", "visitante": "Guarani", "placar": "0 x 0"},
        {"mandante": "Mirassol", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Mirassol", "visitante": "Juventus", "placar": "0 x 0"},
        {"mandante": "Mirassol", "visitante": "Ferroviária", "placar": "0 x 0"},

        # GUARANI
        {"mandante": "Guarani", "visitante": "Primavera", "placar": "0 x 0"},
        {"mandante": "Guarani", "visitante": "Ferroviária", "placar": "0 x 0"},
        {"mandante": "Guarani", "visitante": "Noroeste", "placar": "0 x 0"},

        # PRIMAVERA
        {"mandante": "Primavera", "visitante": "São Bernardo", "placar": "0 x 0"},
        {"mandante": "Primavera", "visitante": "Noroeste", "placar": "0 x 0"},

        # SÃO BERNARDO
        {"mandante": "São Bernardo", "visitante": "Juventus", "placar": "0 x 0"},
        {"mandante": "São Bernardo", "visitante": "Ferroviária", "placar": "0 x 0"},
        {"mandante": "São Bernardo", "visitante": "Noroeste", "placar": "0 x 0"},

        # JUVENTUS
        {"mandante": "Juventus", "visitante": "Ferroviária", "placar": "0 x 0"},
        {"mandante": "Juventus", "visitante": "Noroeste", "placar": "0 x 0"},

        # FERROVIÁRIA
        {"mandante": "Ferroviária", "visitante": "Noroeste", "placar": "0 x 0"}
    ]
    
    partidas_enriquecidas = []
    for jogo in confrontos_iniciais:
        mandante = jogo["mandante"]
        visitante = jogo["visitante"]
        partidas_enriquecidas.append({
            "mandante": mandante,
            "visitante": visitante,
            "escudo_mandante": obter_escudo_clube(mandante),
            "escudo_visitante": obter_escudo_clube(visitante),
            "placar": jogo["placar"]
        })
    return partidas_enriquecidas
