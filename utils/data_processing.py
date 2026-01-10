"""
Procesamiento y transformación de datos de NBA
"""

import pandas as pd
from config import COLUMNAS_SELECCIONADAS


def procesar_datos_nba(df_nba):
    """
    Procesa y formatea los datos obtenidos de la API de NBA.
    
    Args:
        df_nba (pd.DataFrame): DataFrame crudo con datos de la API
        
    Returns:
        pd.DataFrame: DataFrame procesado con columnas renombradas y métricas calculadas
    """
    if df_nba.empty:
        return df_nba
    
    # Seleccionar y renombrar columnas
    columnas_a_usar = [col for col in COLUMNAS_SELECCIONADAS.keys() if col in df_nba.columns]
    df_nba = df_nba[columnas_a_usar].rename(columns=COLUMNAS_SELECCIONADAS)
    
    # Calcular AST/TO si las columnas existen
    if 'Asistencias' in df_nba.columns and 'Pérdidas' in df_nba.columns:
        df_nba['AST/TO'] = df_nba['Asistencias'] / df_nba['Pérdidas'].replace(0, 1)  # Evitar división por cero
    
    return df_nba


def preparar_comparacion(datos_a, datos_b, equipo_a, equipo_b):
    """
    Prepara un DataFrame para la comparación entre dos equipos.
    
    Args:
        datos_a (pd.Series): Datos del equipo A
        datos_b (pd.Series): Datos del equipo B
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        pd.DataFrame: DataFrame con la comparación entre equipos
    """
    comparacion_df = pd.DataFrame({
        equipo_a: datos_a,
        equipo_b: datos_b
    })
    
    # Excluir columnas no relevantes para la comparación
    from config import COLUMNAS_EXCLUIDAS_COMPARACION
    columnas_a_excluir = [col for col in COLUMNAS_EXCLUIDAS_COMPARACION if col in comparacion_df.index]
    comparacion_df = comparacion_df.drop(columnas_a_excluir)
    
    return comparacion_df

