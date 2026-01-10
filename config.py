"""
Configuración y constantes de la aplicación de Análisis NBA
"""

# Configuración de la aplicación
APP_TITLE = "ANALISIS DE DATOS V ALPHA 1.0"
APP_PAGE_TITLE = "Análisis NBA"

# Configuración de la API de NBA
NBA_API_BASE_URL = 'https://stats.nba.com/stats/leaguedashteamstats'
NBA_LEAGUE_ID = '00'
NBA_DEFAULT_SEASON_TYPE = 'Regular Season'

# Headers para las solicitudes HTTP
NBA_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}

# Timeouts para solicitudes
REQUEST_CONNECT_TIMEOUT = 10
REQUEST_READ_TIMEOUT = 25
NBA_API_TIMEOUT = 30
VALIDATION_TIMEOUT = 10

# Configuración de retry
RETRY_TOTAL = 2
RETRY_BACKOFF_FACTOR = 1
RETRY_STATUS_FORCELIST = [429, 500, 502, 503, 504]

# Configuración de cache (en segundos)
CACHE_DATA_TTL = 3600  # 1 hora para datos de equipos
CACHE_SEASON_VALIDATION_TTL = 86400  # 24 horas para validación de temporadas

# Mapeo de columnas a mostrar
COLUMNAS_SELECCIONADAS = {
    'TEAM_NAME': 'Equipo',
    'GP': 'Juegos Jugados',
    'W': 'Victorias',
    'L': 'Derrotas',
    'W_PCT': 'Porc. Victoria',
    'PACE': 'Ritmo de Juego', 
    'E_OFF_RATING': 'Rating Ofensivo', 
    'E_DEF_RATING': 'Rating Defensivo',
    'AST': 'Asistencias',
    'TOV': 'Pérdidas',
    'FG3_PCT': '3P%'
}

# Columnas a excluir de la comparación
COLUMNAS_EXCLUIDAS_COMPARACION = ['Equipo', 'Juegos Jugados', 'Victorias', 'Derrotas']

# Equipos por defecto
DEFAULT_TEAM_A = 'Boston Celtics'
DEFAULT_TEAM_B = 'Denver Nuggets'

# Número de temporadas recientes a mostrar
NUM_TEMPORADAS_RECIENTES = 4

