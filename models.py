from pydantic import BaseModel
from typing import List, Optional

class EventoPartida(BaseModel):
    minuto: int
    acrescimo: Optional[int] = None
    tipo: str  # "gol", "cartao_amarelo", "cartao_vermelho", "substituicao"
    detalhe: str
    equipe: str
    jogador: str

class PartidaResponse(BaseModel):
    id_partida: str
    rodada: int
    status: str  # "NS" (Agendado), "LIVE" (Ao vivo), "HT" (Intervalo), "FT" (Encerrado)
    status_descricao: str  # "Agendado", "Em andamento", "Intervalo em descanso", "Encerrado"
    data_hora: str
    estadio: Optional[str] = None
    mandante: str
    escudo_mandante: str
    visitante: str
    escudo_visitante: str
    placar_mandante: int = 0
    placar_visitante: int = 0
    acrescimo_1t: Optional[int] = None
    acrescimo_2t: Optional[int] = None
    eventos: List[EventoPartida] = []

class TabelaPosicao(BaseModel):
    posicao: int
    clube: str
    escudo: str
    pontos: int
    jogos: int
    vitorias: int
    empates: int
    derrotas: int
    saldo_gols: int
    zona: str  # "normal" ou "rebaixamento"
    cor_destaque: str  # "neutro" ou "vermelho"