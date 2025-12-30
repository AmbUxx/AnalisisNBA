import streamlit as st
import pandas as pd
# Eliminamos la importación de nba_api.stats.endpoints
import plotly.express as px

import numpy as np
import requests # <-- Nueva importación clave para acceder directamente a la API

# --- Configuración de la Aplicación ---
st.set_page_config(layout="wide", page_title="Análisis NBA")

# --- Función de Predicción ---
def predecir_probabilidad(rating_neto_a, rating_neto_b):
    """
    Calcula una probabilidad simple de victoria basada en la diferencia de Ratings Netos.
    Usa una función logística simplificada.
    """
    diferencia = rating_neto_a - rating_neto_b
    probabilidad_a = 1 / (1 + np.exp(-diferencia / 10))
    return probabilidad_a

# --- Función de Obtención de Datos (Solución Final con requests) ---
# --- Función de Obtención de Datos (Solución Final: Evitar Bloqueo) ---
@st.cache_data
def obtener_datos_nba(temporada='2023-24'):
    """
    Obtiene y procesa las estadísticas avanzadas directamente desde la URL de la NBA.
    Se han añadido más headers para simular un navegador real y evitar timeouts/bloqueos.
    """
    
    # 1. Definición de Parámetros y URL de la API (Medida de Tipo Avanzada)
    # Aumentamos los headers para que la solicitud parezca más legítima
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nba.com/', # <-- Crucial: Simular que navegamos desde la web de la NBA
        'Connection': 'keep-alive'
    }
    
    params = {
        'LeagueID': '00',
        'MeasureType': 'Advanced', 
        'PerMode': 'PerGame',      
        'Season': temporada,
        'SeasonType': 'Regular Season',
        'PORound': '0'
    }

    url = 'https://stats.nba.com/stats/leaguedashteamstats'
    
    try:
        # 2. Realizar la solicitud HTTP directa con timeout aumentado
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status() 

        # ... (El resto del código de parsing JSON y DataFrame sigue igual)
        data = response.json()
        team_stats_data = data['resultSets'][0]
        df_nba = pd.DataFrame(team_stats_data['rowSet'], columns=team_stats_data['headers'])

        # 4. Seleccionar y renombrar columnas clave
        columnas_seleccionadas = {
            # ... (se mantiene la lista de columnas)
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
        
        columnas_a_usar = [col for col in columnas_seleccionadas.keys() if col in df_nba.columns]
        df_nba = df_nba[columnas_a_usar].rename(columns=columnas_seleccionadas)
        df_nba['AST/TO'] = df_nba['Asistencias'] / df_nba['Pérdidas']
        
        return df_nba
        
    except requests.exceptions.RequestException as e:
        # Mensaje de error ajustado para indicar un bloqueo de red
        st.error(f"Error de Bloqueo de Conexión: La solicitud fue rechazada o superó el tiempo de espera. Causa: {e}. Por favor, desactiva tu VPN/Firewall e inténtalo de nuevo.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error general al procesar datos: {e}") 
        return pd.DataFrame()


# --- Lógica Principal de la Aplicación ---
def main():
    st.title("ANALISIS DE DATOS V ALPHA 1.0")
    st.markdown("---")

    # Obtener el DataFrame
    # ELIMINAMOS LA IMPORTACIÓN DE NBA_API AQUÍ, pero la llamaremos más abajo.
    # Necesitas eliminar 'from nba_api.stats.endpoints import leaguedashteamstats' de la parte superior del script original
    df_nba = obtener_datos_nba(temporada='2023-24') 

    if df_nba.empty:
        st.stop()
        
    # El resto del código principal (sidebar, filtros, pestañas y predicción) es CORRECTO y se mantiene.
    
    equipos_disponibles = sorted(df_nba['Equipo'].unique().tolist())

    # --- Sidebar para Selección de Equipos ---
    # ... (código del sidebar)
    st.sidebar.header("Selección de Equipos")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        equipo_a = st.selectbox(
            "Equipo A",
            equipos_disponibles,
            index=equipos_disponibles.index('Boston Celtics') if 'Boston Celtics' in equipos_disponibles else 0
        )

    with col2:
        default_index_b = equipos_disponibles.index('Denver Nuggets') if 'Denver Nuggets' in equipos_disponibles else 1
        equipo_b = st.selectbox(
            "Equipo B",
            equipos_disponibles,
            index=default_index_b
        )

    # --- Filtrar Datos ---
    datos_a = df_nba[df_nba['Equipo'] == equipo_a].iloc[0]
    datos_b = df_nba[df_nba['Equipo'] == equipo_b].iloc[0]

    comparacion_df = pd.DataFrame({
        equipo_a: datos_a,
        equipo_b: datos_b
    }).drop(['Equipo', 'Juegos Jugados', 'Victorias', 'Derrotas'])

    # --- Pestañas de Visualización ---
    tab1, tab2, tab3 = st.tabs(["Tabla de Comparación", "Patrones de Juego (Ritmo/Eficiencia)", "Métricas de Creación de Juego"])

    # Pestaña 1: Tabla Completa
    with tab1:
        st.header(f"Comparación Métrica a Métrica: {equipo_a} vs {equipo_b}")
        st.dataframe(comparacion_df.T.style.highlight_max(axis=0, color='background-color: lightgreen'), use_container_width=True)
        st.caption("Los valores más altos en cada métrica están resaltados en verde.")

    # Pestaña 2: Patrones de Juego (Ritmo y Eficiencia)
    with tab2:
        st.header("Análisis de Eficiencia y Patrones (Ratings y Ritmo)")
        
        ratings_data = comparacion_df.loc[['Rating Ofensivo', 'Rating Defensivo']].T.reset_index().rename(columns={'index': 'Equipo'})
        fig_ratings = px.bar(
            ratings_data, 
            x='Equipo', 
            y=['Rating Ofensivo', 'Rating Defensivo'], 
            barmode='group',
            title='Rating Ofensivo y Defensivo (Puntos por 100 Posesiones)',
            color_discrete_map={'Rating Ofensivo': 'green', 'Rating Defensivo': 'red'}
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        pace_data = comparacion_df.loc['Ritmo de Juego'].T.reset_index().rename(columns={'index': 'Equipo'})
        fig_pace = px.bar(
            pace_data, 
            x=pace_data.index, 
            y='Ritmo de Juego',
            title='Ritmo de Juego (Posesiones por 48 min)',
            labels={'Ritmo de Juego': 'Pace'}
        )
        st.plotly_chart(fig_pace, use_container_width=True)

    # Pestaña 3: Creación de Juego
    with tab3:
        st.header("Análisis de Creación de Juego (AST/TO y 3P%)")
        
        ast_to_data = comparacion_df.loc['AST/TO'].T.reset_index().rename(columns={'index': 'Equipo'})
        fig_ast_to = px.bar(
            ast_to_data, 
            x=ast_to_data.index, 
            y='AST/TO',
            title='Ratio Asistencias / Pérdidas (AST/TO)',
            labels={'AST/TO': 'Relación AST/TO'}
        )
        st.plotly_chart(fig_ast_to, use_container_width=True)
        
        p3_data = comparacion_df.loc['3P%'].T.reset_index().rename(columns={'index': 'Equipo'})
        fig_p3 = px.bar(
            p3_data, 
            x=p3_data.index, 
            y='3P%',
            title='Porcentaje de Tiros de 3 Puntos (3P%)',
            labels={'3P%': '3P%'}
        )
        st.plotly_chart(fig_p3, use_container_width=True)
        
    # --- Sección de Probabilidad de Victoria ---
    st.markdown("---")
    st.header("🔮 Posibilidad de Victoria (Modelo Básico)")
    
    # 1. Calcular Rating Neto para cada equipo
    net_rating_a = datos_a['Rating Ofensivo'] - datos_a['Rating Defensivo']
    net_rating_b = datos_b['Rating Ofensivo'] - datos_b['Rating Defensivo']

    # 2. Obtener la probabilidad
    prob_a_decimal = predecir_probabilidad(net_rating_a, net_rating_b)
    prob_b_decimal = 1 - prob_a_decimal

    prob_a_porc = round(prob_a_decimal * 100, 1)
    prob_b_porc = round(prob_b_decimal * 100, 1)

    # 3. Visualizar el resultado
    col_prob_a, col_prob_b = st.columns(2)

    with col_prob_a:
        st.metric(
            label=f"Probabilidad de Ganar: {equipo_a}", 
            value=f"{prob_a_porc}%",
            delta=f"Net Rating: {net_rating_a:.2f}"
        )
    
    with col_prob_b:
        st.metric(
            label=f"Probabilidad de Ganar: {equipo_b}", 
            value=f"{prob_b_porc}%",
            delta=f"Net Rating: {net_rating_b:.2f}"
        )
    
    st.markdown(f"> **Interpretación:** Este modelo simple predice la victoria basándose en la diferencia en el **Rating Neto** (la eficiencia general del equipo). {equipo_a} ({net_rating_a:.2f}) tiene una probabilidad de **{prob_a_porc}%** de ganar contra {equipo_b} ({net_rating_b:.2f}).")
        
if __name__ == "__main__":
    main()