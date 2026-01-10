"""
Modelos de predicción y cálculo de métricas
"""

import numpy as np


def calcular_net_rating(rating_ofensivo, rating_defensivo):
    """
    Calcula el Rating Neto de un equipo.
    
    Args:
        rating_ofensivo (float): Rating ofensivo del equipo
        rating_defensivo (float): Rating defensivo del equipo
        
    Returns:
        float: Rating neto (ofensivo - defensivo)
    """
    return rating_ofensivo - rating_defensivo


def predecir_probabilidad(rating_neto_a, rating_neto_b):
    """
    Calcula una probabilidad simple de victoria basada en la diferencia de Ratings Netos.
    Usa una función logística simplificada.
    
    Args:
        rating_neto_a (float): Rating neto del equipo A
        rating_neto_b (float): Rating neto del equipo B
        
    Returns:
        float: Probabilidad de victoria del equipo A (entre 0 y 1)
    """
    diferencia = rating_neto_a - rating_neto_b
    probabilidad_a = 1 / (1 + np.exp(-diferencia / 10))
    return probabilidad_a

