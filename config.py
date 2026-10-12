class Settings:
    PROJECT_NAME: str = "API Campeonato Paulista 2027 - ESPN"
    VERSION: str = "1.0.0"
    
    # Endpoint público e aberto da ESPN (mesmo padrão usado na Série A e B)
    ESPN_PAULISTA_URL: str = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.paulista/scoreboard"

settings = Settings()