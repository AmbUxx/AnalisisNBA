"""
Utilidades para manejo de temporadas de la NBA
"""

from datetime import datetime
import streamlit as st
from config import VALIDATION_TIMEOUT

try:
    from nba_api.stats.endpoints import leaguedashteamstats
    NBA_API_AVAILABLE = True
except ImportError:
    NBA_API_AVAILABLE = False


def obtener_temporada_actual():
    """
    Determina automáticamente la temporada actual de la NBA.
    La temporada NBA generalmente va de octubre (año X) a junio (año X+1).
    Ejemplo: Octubre 2024 - Junio 2025 = temporada "2024-25"
    
    Returns:
        str: Temporada actual en formato "YYYY-YY"
    """
    ahora = datetime.now()
    mes_actual = ahora.month
    año_actual = ahora.year
    
    # Si estamos entre octubre y diciembre, la temporada comenzó este año
    # Si estamos entre enero y junio, la temporada comenzó el año pasado
    if mes_actual >= 10:  # Octubre, Noviembre, Diciembre
        año_inicio = año_actual
    else:  # Enero - Septiembre
        año_inicio = año_actual - 1
    
    año_fin = año_inicio + 1
    # Formato: "2024-25"
    temporada = f"{año_inicio}-{str(año_fin)[-2:]}"
    
    return temporada


@st.cache_data(ttl=86400)  # Cache por 24 horas
def validar_temporada_disponible(temporada):
    """
    Verifica si una temporada está disponible en la API de NBA.
    
    Args:
        temporada (str): Temporada a validar en formato "YYYY-YY"
        
    Returns:
        bool: True si la temporada está disponible, False en caso contrario
    """
    if not NBA_API_AVAILABLE:
        return True  # Si no tenemos nba_api, asumimos que es válida
    
    try:
        stats = leaguedashteamstats.LeagueDashTeamStats(
            league_id_nullable='00',
            measure_type_detailed_defense='Base',
            per_mode_detailed='PerGame',
            season=temporada,
            season_type_all_star='Regular Season',
            timeout=VALIDATION_TIMEOUT
        )
        df = stats.get_data_frames()[0]
        return len(df) > 0  # Si tiene datos, la temporada existe
    except Exception:
        return False


def generar_lista_temporadas(temporada_base, num_temporadas=4):
    """
    Genera una lista de temporadas recientes basada en una temporada base.
    
    Args:
        temporada_base (str): Temporada base en formato "YYYY-YY"
        num_temporadas (int): Número de temporadas a generar
        
    Returns:
        list: Lista de temporadas en formato ["YYYY-YY", ...]
    """
    año_inicio = int(temporada_base.split('-')[0])
    temporadas = []
    
    for i in range(num_temporadas):
        año = año_inicio - i
        año_sig = año + 1
        temporadas.append(f"{año}-{str(año_sig)[-2:]}")
    
    return temporadas


def obtener_temporada_disponible_mas_reciente():
    """
    Obtiene la temporada más reciente que esté disponible en la API.
    
    Returns:
        str: Temporada más reciente disponible en formato "YYYY-YY"
    """
    temporada_actual = obtener_temporada_actual()
    
    # Si la temporada actual está disponible, usarla
    if validar_temporada_disponible(temporada_actual):
        return temporada_actual
    
    # Si no, usar la temporada anterior
    año_inicio = int(temporada_actual.split('-')[0])
    año_anterior = año_inicio - 1
    temporada_anterior = f"{año_anterior}-{str(año_inicio)[-2:]}"
    
    return temporada_anterior

