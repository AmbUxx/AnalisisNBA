"""
Funciones para crear visualizaciones de datos de NBA - Estilo Betting/Fintech
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def crear_grafico_ratings(comparacion_df, equipo_a, equipo_b):
    """
    Crea un gráfico de barras mejorado comparando ratings ofensivos y defensivos.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    ratings_data = comparacion_df.loc[['Rating Ofensivo', 'Rating Defensivo']].T
    ratings_data.index = [equipo_a, equipo_b]
    
    # Crear gráfico con valores exactos
    fig = go.Figure()
    
    # Datos
    equipos = [equipo_a, equipo_b]
    off_ratings = [ratings_data.loc[eq, 'Rating Ofensivo'] for eq in equipos]
    def_ratings = [ratings_data.loc[eq, 'Rating Defensivo'] for eq in equipos]
    
    # Barras de Rating Ofensivo (verde neón)
    fig.add_trace(go.Bar(
        name='Rating Ofensivo',
        x=equipos,
        y=off_ratings,
        marker_color='#00ff88',
        marker_line_color='#00d9ff',
        marker_line_width=2,
        text=[f'{val:.2f}' for val in off_ratings],
        textposition='outside',
        textfont=dict(size=14, color='#00ff88', family='monospace'),
        hovertemplate='<b>%{x}</b><br>Rating Ofensivo: %{y:.2f}<extra></extra>'
    ))
    
    # Barras de Rating Defensivo (rojo)
    fig.add_trace(go.Bar(
        name='Rating Defensivo',
        x=equipos,
        y=def_ratings,
        marker_color='#ff4444',
        marker_line_color='#ff8c00',
        marker_line_width=2,
        text=[f'{val:.2f}' for val in def_ratings],
        textposition='outside',
        textfont=dict(size=14, color='#ff4444', family='monospace'),
        hovertemplate='<b>%{x}</b><br>Rating Defensivo: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>⚡ Ratings Ofensivo vs Defensivo</b>',
            font=dict(size=18, color='#00d9ff', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=13, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)'
        ),
        yaxis=dict(
            title=dict(text='Puntos por 100 Posesiones', font=dict(size=12, color='#b4b4ff')),
            tickfont=dict(size=11, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)',
            zeroline=False
        ),
        barmode='group',
        plot_bgcolor='#0f1422',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#b4b4ff'),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(180, 180, 255, 0.3)'
        ),
        margin=dict(l=20, r=20, t=80, b=50)
    )
    
    return fig


def crear_grafico_pace(comparacion_df, equipo_a, equipo_b):
    """
    Crea un gráfico de barras mejorado comparando el ritmo de juego.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    pace_a = comparacion_df.loc['Ritmo de Juego', equipo_a]
    pace_b = comparacion_df.loc['Ritmo de Juego', equipo_b]
    
    # Determinar mejor (mayor pace generalmente es mejor, pero depende del estilo de juego)
    mejor_pace = max(pace_a, pace_b)
    
    fig = go.Figure()
    
    # Colores según qué equipo tiene mayor pace
    color_a = '#00ff88' if pace_a >= pace_b else '#b4b4ff'
    color_b = '#00ff88' if pace_b >= pace_a else '#b4b4ff'
    
    fig.add_trace(go.Bar(
        x=[equipo_a, equipo_b],
        y=[pace_a, pace_b],
        marker_color=[color_a, color_b],
        marker_line_color='#00d9ff',
        marker_line_width=2,
        text=[f'{pace_a:.2f}', f'{pace_b:.2f}'],
        textposition='outside',
        textfont=dict(size=16, color='#00d9ff', family='monospace', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Pace: %{y:.2f} posesiones/48min<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>🏃 Ritmo de Juego (Pace)</b>',
            font=dict(size=18, color='#00d9ff', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=13, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)'
        ),
        yaxis=dict(
            title=dict(text='Posesiones por 48 minutos', font=dict(size=12, color='#b4b4ff')),
            tickfont=dict(size=11, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)',
            zeroline=False
        ),
        plot_bgcolor='#0f1422',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        height=450,
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=50)
    )
    
    return fig


def crear_grafico_ast_to(comparacion_df, equipo_a, equipo_b):
    """
    Crea un gráfico de barras mejorado comparando el ratio AST/TO.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    ast_to_a = comparacion_df.loc['AST/TO', equipo_a]
    ast_to_b = comparacion_df.loc['AST/TO', equipo_b]
    
    # Mayor es mejor
    mejor_ast_to = max(ast_to_a, ast_to_b)
    
    fig = go.Figure()
    
    color_a = '#00ff88' if ast_to_a >= ast_to_b else '#b4b4ff'
    color_b = '#00ff88' if ast_to_b >= ast_to_a else '#b4b4ff'
    
    fig.add_trace(go.Bar(
        x=[equipo_a, equipo_b],
        y=[ast_to_a, ast_to_b],
        marker_color=[color_a, color_b],
        marker_line_color='#00d9ff',
        marker_line_width=2,
        text=[f'{ast_to_a:.2f}', f'{ast_to_b:.2f}'],
        textposition='outside',
        textfont=dict(size=16, color='#00d9ff', family='monospace', weight='bold'),
        hovertemplate='<b>%{x}</b><br>AST/TO: %{y:.2f}<br>Mayor es mejor<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>🎯 Ratio Asistencias/Pérdidas (AST/TO)</b>',
            font=dict(size=18, color='#00d9ff', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=13, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)'
        ),
        yaxis=dict(
            title=dict(text='Relación AST/TO', font=dict(size=12, color='#b4b4ff')),
            tickfont=dict(size=11, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)',
            zeroline=False
        ),
        plot_bgcolor='#0f1422',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        height=450,
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=50)
    )
    
    return fig


def crear_grafico_3p(comparacion_df, equipo_a, equipo_b):
    """
    Crea un gráfico de barras mejorado comparando el porcentaje de tiros de 3 puntos.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de Plotly
    """
    p3_a = comparacion_df.loc['3P%', equipo_a]
    p3_b = comparacion_df.loc['3P%', equipo_b]
    
    # Mayor es mejor
    mejor_p3 = max(p3_a, p3_b)
    
    fig = go.Figure()
    
    color_a = '#00ff88' if p3_a >= p3_b else '#b4b4ff'
    color_b = '#00ff88' if p3_b >= p3_a else '#b4b4ff'
    
    fig.add_trace(go.Bar(
        x=[equipo_a, equipo_b],
        y=[p3_a, p3_b],
        marker_color=[color_a, color_b],
        marker_line_color='#00d9ff',
        marker_line_width=2,
        text=[f'{p3_a:.1%}', f'{p3_b:.1%}'],
        textposition='outside',
        textfont=dict(size=16, color='#00d9ff', family='monospace', weight='bold'),
        hovertemplate='<b>%{x}</b><br>3P%: %{y:.1%}<br>Mayor es mejor<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>🏀 Porcentaje de Tiros de 3 Puntos</b>',
            font=dict(size=18, color='#00d9ff', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=13, color='#b4b4ff', family='monospace'),
            gridcolor='rgba(180, 180, 255, 0.1)'
        ),
        yaxis=dict(
            title=dict(text='Porcentaje de Efectividad', font=dict(size=12, color='#b4b4ff')),
            tickfont=dict(size=11, color='#b4b4ff', family='monospace'),
            tickformat='.0%',
            gridcolor='rgba(180, 180, 255, 0.1)',
            zeroline=False
        ),
        plot_bgcolor='#0f1422',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        height=450,
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=50)
    )
    
    return fig
