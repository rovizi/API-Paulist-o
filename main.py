# -*- coding: utf-8 -*-

"""
services.py - Fonte da verdade para dados do Paulistão 2027.
Gerencia os escudos padronizados dos 16 clubes da Série A1 e a inicialização de dados da API.
"""

# Dicionário oficial e padronizado com os escudos tradicionais dos 16 clubes da Série A1
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
    "São Bernardo": "https://i.postimg.cc/g23dxKV6/Sao-Bernardo-FC-2020-crest.png",
    "Primavera": "https://i.postimg.cc/SNt2ktnW/logo-ebook.png",
    "Capivariano": "https://i.postimg.cc/nL84knQn/capivariano.png",
    "Novorizontino": "https://i.postimg.cc/tJLJj4bZ/images-removebg-preview.png",
    "Ferroviária": "https://i.postimg.cc/66S3Ckt7/ad92fcd869cb0047d7c4af335b575762-removebg-preview.png",
    "Noroeste": "https://i.postimg.cc/L8PCRCtM/9500b1cc3476659e93ed698e386b2a95-removebg-preview.png",
    "Juventus": "https://i.postimg.cc/T1ySbRDP/ae184f0d31dcb85851aaab1fd2432e40.png"
}


def obter_escudo_clube(nome_clube: str) -> str:
    """
    Retorna a URL oficial do escudo do clube.
    """
    return ESCUDOS_CUSTOMIZADOS.get(nome_clube, "")


def zerar_estatisticas_clube(nome_clube: str) -> dict:
    """
    Retorna a estrutura de dados de um clube zerada para o estado pré-torneio.
    """
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
    """
    Gera a tabela de classificação inicial com todos os 16 clubes
    devidamente mapeados e com estatísticas zeradas.
    """
    return [zerar_estatisticas_clube(clube) for clube in ESCUDOS_CUSTOMIZADOS.keys()]


def obter_partidas_paulistao() -> list:
    """
    Retorna a lista de partidas injetando os escudos corretos dos mandantes e visitantes.
    """
    # Se houver uma lista base de partidas no seu projeto, você pode mapeá-la aqui.
    # Caso retorne vazio ou lista de confrontos, garanta o formato compatível com o main.py.
    return []
