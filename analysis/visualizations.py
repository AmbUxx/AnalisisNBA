"""
Funciones para crear visualizaciones de datos de NBA
"""

import pandas as pd
import plotly.express as px


def crear_grafico_ratings(comparacion_df):
    """
    Crea un gráfico de barras comparando ratings ofensivos y defensivos.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    ratings_data = comparacion_df.loc[['Rating Ofensivo', 'Rating Defensivo']].T.reset_index().rename(columns={'index': 'Equipo'})
    
    fig = px.bar(
        ratings_data, 
        x='Equipo', 
        y=['Rating Ofensivo', 'Rating Defensivo'], 
        barmode='group',
        title='Rating Ofensivo y Defensivo (Puntos por 100 Posesiones)',
        color_discrete_map={
            'Rating Ofensivo': '#28a745', 
            'Rating Defensivo': '#dc3545'
        },
        labels={
            'value': 'Rating',
            'variable': 'Tipo de Rating'
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def crear_grafico_pace(comparacion_df):
    """
    Crea un gráfico de barras comparando el ritmo de juego.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    pace_data = comparacion_df.loc['Ritmo de Juego'].T.reset_index().rename(columns={'index': 'Equipo'})
    
    fig = px.bar(
        pace_data, 
        x=pace_data.index, 
        y='Ritmo de Juego',
        title='Ritmo de Juego (Posesiones por 48 min)',
        labels={'Ritmo de Juego': 'Pace'},
        color='Ritmo de Juego',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        showlegend=False
    )
    
    return fig


def crear_grafico_ast_to(comparacion_df):
    """
    Crea un gráfico de barras comparando el ratio AST/TO.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    ast_to_data = comparacion_df.loc['AST/TO'].T.reset_index().rename(columns={'index': 'Equipo'})
    
    fig = px.bar(
        ast_to_data, 
        x=ast_to_data.index, 
        y='AST/TO',
        title='Ratio Asistencias / Pérdidas (AST/TO)',
        labels={'AST/TO': 'Relación AST/TO'},
        color='AST/TO',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        showlegend=False
    )
    
    return fig


def crear_grafico_3p(comparacion_df):
    """
    Crea un gráfico de barras comparando el porcentaje de tiros de 3 puntos.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    p3_data = comparacion_df.loc['3P%'].T.reset_index().rename(columns={'index': 'Equipo'})
    
    fig = px.bar(
        p3_data, 
        x=p3_data.index, 
        y='3P%',
        title='Porcentaje de Tiros de 3 Puntos (3P%)',
        labels={'3P%': '3P%'},
        color='3P%',
        color_continuous_scale='Oranges'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        showlegend=False,
        yaxis=dict(tickformat='.1%')
    )
    
    return fig

