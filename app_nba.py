import streamlit as st
import pandas as pd
# Eliminamos la importación de nba_api.stats.endpoints
import plotly.express as px

import numpy as np
from datetime import datetime
import requests # <-- Nueva importación clave para acceder directamente a la API
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
try:
    from nba_api.stats.endpoints import leaguedashteamstats
    NBA_API_AVAILABLE = True
except ImportError:
    NBA_API_AVAILABLE = False

# --- Configuración de la Aplicación ---
st.set_page_config(layout="wide", page_title="Análisis NBA")

# --- Función para obtener la temporada actual automáticamente ---
def obtener_temporada_actual():
    """
    Determina automáticamente la temporada actual de la NBA.
    La temporada NBA generalmente va de octubre (año X) a junio (año X+1).
    Ejemplo: Octubre 2024 - Junio 2025 = temporada "2024-25"
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

# --- Función para validar si una temporada existe en la API ---
@st.cache_data(ttl=86400)  # Cache por 24 horas (las temporadas no cambian tan frecuentemente)
def validar_temporada_disponible(temporada):
    """
    Verifica si una temporada está disponible en la API de NBA.
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
            timeout=10
        )
        df = stats.get_data_frames()[0]
        return len(df) > 0  # Si tiene datos, la temporada existe
    except:
        return False

# --- Función de Predicción ---
def predecir_probabilidad(rating_neto_a, rating_neto_b):
    """
    Calcula una probabilidad simple de victoria basada en la diferencia de Ratings Netos.
    Usa una función logística simplificada.
    """
    diferencia = rating_neto_a - rating_neto_b
    probabilidad_a = 1 / (1 + np.exp(-diferencia / 10))
    return probabilidad_a

# --- Función de Obtención de Datos (Solución con múltiples métodos) ---
@st.cache_data(ttl=3600)  # Cache por 1 hora para mantener datos actualizados
def obtener_datos_nba(temporada='2023-24'):
    """
    Obtiene y procesa las estadísticas avanzadas desde la API de NBA.
    Intenta primero con requests directo, y si falla, usa la librería nba_api como alternativa.
    """
    
    # Método 1: Intentar con requests directo
    session = requests.Session()
    retry_strategy = Retry(
        total=2,  # Reducir reintentos para fallar más rápido y probar alternativa
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    headers = {
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
        # Intentar método 1: requests directo
        response = session.get(url, headers=headers, params=params, timeout=(10, 25), verify=True)
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
                    league_id_nullable='00',
                    measure_type_detailed_defense='Base',
                    per_mode_detailed='PerGame',
                    season=temporada,
                    season_type_all_star='Regular Season',
                    timeout=30
                )
                df_base = stats_base.get_data_frames()[0]
                
                # Obtener estadísticas avanzadas (PACE, Ratings)
                stats_advanced = leaguedashteamstats.LeagueDashTeamStats(
                    league_id_nullable='00',
                    measure_type_detailed_defense='Advanced',
                    per_mode_detailed='PerGame',
                    season=temporada,
                    season_type_all_star='Regular Season',
                    timeout=30
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

    # Procesar y formatear los datos (igual para ambos métodos)
    columnas_seleccionadas = {
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
    
    # Validar que las columnas necesarias existen antes de calcular AST/TO
    if 'Asistencias' in df_nba.columns and 'Pérdidas' in df_nba.columns:
        df_nba['AST/TO'] = df_nba['Asistencias'] / df_nba['Pérdidas'].replace(0, 1)  # Evitar división por cero
    
    return df_nba


# --- Lógica Principal de la Aplicación ---
def main():
    st.title("ANALISIS DE DATOS V ALPHA 1.0")
    st.markdown("---")

    # Determinar automáticamente la temporada actual
    temporada_actual = obtener_temporada_actual()
    
    # Verificar si la temporada actual está disponible, si no, usar la anterior
    temporada_a_usar = temporada_actual
    if not validar_temporada_disponible(temporada_actual):
        # Si la temporada actual no está disponible (todavía no empezó), usar la anterior
        año_inicio = int(temporada_actual.split('-')[0])
        año_fin = año_inicio
        año_anterior = año_inicio - 1
        temporada_a_usar = f"{año_anterior}-{str(año_fin)[-2:]}"
        st.info(f"ℹ️ La temporada {temporada_actual} aún no está disponible. Mostrando datos de {temporada_a_usar}.")

    # Selector de temporada en el sidebar (opcional, para cambiar si se desea)
    st.sidebar.header("⚙️ Configuración")
    
    # Generar lista de temporadas recientes
    año_inicio = int(temporada_a_usar.split('-')[0])
    temporadas_disponibles = []
    for i in range(4):  # Últimas 4 temporadas
        año = año_inicio - i
        año_sig = año + 1
        temporadas_disponibles.append(f"{año}-{str(año_sig)[-2:]}")
    
    # Encontrar el índice de la temporada actual
    try:
        indice_default = temporadas_disponibles.index(temporada_a_usar)
    except ValueError:
        indice_default = 0
    
    temporada_seleccionada = st.sidebar.selectbox(
        "Temporada",
        temporadas_disponibles,
        index=indice_default,
        help="Por defecto se usa la temporada más reciente disponible. Puedes cambiar manualmente si lo deseas."
    )
    
    st.sidebar.caption(f"📊 Datos actualizados de la temporada {temporada_seleccionada}")
    st.sidebar.caption("🔄 Los datos se actualizan automáticamente desde la API oficial de la NBA")
    
    # Botón para forzar actualización de datos
    if st.sidebar.button("🔄 Actualizar Datos Ahora"):
        obtener_datos_nba.clear()  # Limpiar el cache para forzar actualización
        validar_temporada_disponible.clear()  # También limpiar validación de temporada
        st.rerun()

    # Obtener el DataFrame con la temporada seleccionada
    df_nba = obtener_datos_nba(temporada=temporada_seleccionada) 

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
    