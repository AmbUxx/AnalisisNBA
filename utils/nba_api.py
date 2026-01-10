"""
Módulo para conexión y obtención de datos de la API de NBA
"""

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import streamlit as st

from config import (
    NBA_API_BASE_URL,
    NBA_LEAGUE_ID,
    NBA_DEFAULT_SEASON_TYPE,
    NBA_HEADERS,
    REQUEST_CONNECT_TIMEOUT,
    REQUEST_READ_TIMEOUT,
    NBA_API_TIMEOUT,
    RETRY_TOTAL,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_FORCELIST,
    CACHE_DATA_TTL
)

try:
    from nba_api.stats.endpoints import leaguedashteamstats
    NBA_API_AVAILABLE = True
except ImportError:
    NBA_API_AVAILABLE = False


@st.cache_data(ttl=CACHE_DATA_TTL)
def obtener_datos_nba(temporada='2023-24'):
    """
    Obtiene y procesa las estadísticas avanzadas desde la API de NBA.
    Intenta primero con requests directo, y si falla, usa la librería nba_api como alternativa.
    
    Args:
        temporada (str): Temporada a obtener en formato "YYYY-YY"
        
    Returns:
        pd.DataFrame: DataFrame con los datos de los equipos procesados
    """
    
    # Método 1: Intentar con requests directo
    session = requests.Session()
    retry_strategy = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST,
        allowed_methods=["GET", "HEAD"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    params = {
        'LeagueID': NBA_LEAGUE_ID,
        'MeasureType': 'Advanced', 
        'PerMode': 'PerGame',      
        'Season': temporada,
        'SeasonType': NBA_DEFAULT_SEASON_TYPE,
        'PORound': '0'
    }
    
    try:
        # Intentar método 1: requests directo
        response = session.get(
            NBA_API_BASE_URL,
            headers=NBA_HEADERS,
            params=params,
            timeout=(REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT),
            verify=True
        )
        response.raise_for_status()
        data = response.json()
        team_stats_data = data['resultSets'][0]
        df_nba = pd.DataFrame(team_stats_data['rowSet'], columns=team_stats_data['headers'])
        session.close()
        
    except Exception as e:
        session.close()
        
        # Método 2: Usar nba_api como alternativa
        if NBA_API_AVAILABLE:
            try:
                st.info("🔄 Intentando método alternativo con nba_api...")
                
                # Obtener estadísticas base (AST, TOV, FG3_PCT)
                stats_base = leaguedashteamstats.LeagueDashTeamStats(
                    league_id_nullable=NBA_LEAGUE_ID,
                    measure_type_detailed_defense='Base',
                    per_mode_detailed='PerGame',
                    season=temporada,
                    season_type_all_star=NBA_DEFAULT_SEASON_TYPE,
                    timeout=NBA_API_TIMEOUT
                )
                df_base = stats_base.get_data_frames()[0]
                
                # Obtener estadísticas avanzadas (PACE, Ratings)
                stats_advanced = leaguedashteamstats.LeagueDashTeamStats(
                    league_id_nullable=NBA_LEAGUE_ID,
                    measure_type_detailed_defense='Advanced',
                    per_mode_detailed='PerGame',
                    season=temporada,
                    season_type_all_star=NBA_DEFAULT_SEASON_TYPE,
                    timeout=NBA_API_TIMEOUT
                )
                df_advanced = stats_advanced.get_data_frames()[0]
                
                # Combinar ambos DataFrames usando TEAM_ID como clave
                df_nba = pd.merge(
                    df_base[['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'AST', 'TOV', 'FG3_PCT']],
                    df_advanced[['TEAM_ID', 'PACE', 'E_OFF_RATING', 'E_DEF_RATING']],
                    on='TEAM_ID',
                    how='inner'
                )
                
                st.success("✅ Datos obtenidos usando nba_api")
            except Exception as e2:
                st.error(f"❌ Ambos métodos fallaron. Error en nba_api: {type(e2).__name__}: {e2}")
                st.error(f"Error inicial en requests: {type(e).__name__}")
                return pd.DataFrame()
        else:
            st.error(f"❌ Error al obtener datos. Causa: {type(e).__name__}: {e}")
            st.info("💡 Tip: Instala nba_api ejecutando: pip install nba-api")
            return pd.DataFrame()
    
    return df_nba

