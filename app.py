"""
Aplicación principal de Streamlit para Análisis de Datos NBA
"""

import streamlit as st

from config import (
    APP_TITLE,
    APP_PAGE_TITLE,
    DEFAULT_TEAM_A,
    DEFAULT_TEAM_B,
    NUM_TEMPORADAS_RECIENTES
)
from utils import (
    obtener_temporada_actual,
    validar_temporada_disponible,
    generar_lista_temporadas,
    obtener_datos_nba
)
from utils.data_processing import procesar_datos_nba, preparar_comparacion
from analysis.predictions import predecir_probabilidad, calcular_net_rating
from analysis.visualizations import (
    crear_grafico_ratings,
    crear_grafico_pace,
    crear_grafico_ast_to,
    crear_grafico_3p
)
from ui import render_comparison_table, render_simple_header, render_bento_grid, apply_custom_styles

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title=APP_PAGE_TITLE,
    page_icon="🏀",
    initial_sidebar_state="expanded"
)

# Aplicar estilos personalizados
apply_custom_styles()








def render_comparison_tabs(comparacion_df, equipo_a, equipo_b):
    """
    Renderiza las pestañas de comparación con diseño mejorado.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
    """
    tab1, tab2, tab3 = st.tabs([
        "📊 COMPARATIVA",
        "⚡ EFICIENCIA",
        "🎯 CREACIÓN"
    ])
    
    # Pestaña 1: Tabla Completa
    with tab1:
        st.markdown(f"### Comparación Detallada")
        render_comparison_table(comparacion_df, equipo_a, equipo_b)
    
    # Pestaña 2: Patrones de Juego
    with tab2:
        st.markdown("### Eficiencia y Ritmo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_ratings = crear_grafico_ratings(comparacion_df, equipo_a, equipo_b)
            st.plotly_chart(fig_ratings, use_container_width=True)
        
        with col2:
            fig_pace = crear_grafico_pace(comparacion_df, equipo_a, equipo_b)
            st.plotly_chart(fig_pace, use_container_width=True)
        
        with st.expander("ℹ️ Explicación de Métricas"):
            st.markdown("""
            - **Rating Ofensivo**: Puntos anotados por 100 posesiones (mayor es mejor)
            - **Rating Defensivo**: Puntos permitidos por 100 posesiones (menor es mejor)
            - **Pace**: Ritmo de juego medido en posesiones por 48 minutos
            """)
    
    # Pestaña 3: Creación de Juego
    with tab3:
        st.markdown("### Creación de Juego")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_ast_to = crear_grafico_ast_to(comparacion_df, equipo_a, equipo_b)
            st.plotly_chart(fig_ast_to, use_container_width=True)
        
        with col2:
            fig_p3 = crear_grafico_3p(comparacion_df, equipo_a, equipo_b)
            st.plotly_chart(fig_p3, use_container_width=True)
        
        with st.expander("ℹ️ Explicación de Métricas"):
            st.markdown("""
            - **AST/TO**: Relación entre asistencias y pérdidas. Valores más altos indican mejor manejo del balón
            - **3P%**: Porcentaje de efectividad en tiros de 3 puntos. Crítico en el baloncesto moderno
            """)


def render_prediction_section(datos_a, datos_b, equipo_a, equipo_b):
    """
    Renderiza la sección de predicción de victoria con diseño mejorado.
    
    Args:
        datos_a (pd.Series): Datos del equipo A
        datos_b (pd.Series): Datos del equipo B
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
    """
    st.markdown("---")
    st.markdown("## 🔮 Predicción de Resultado")
    
    # Calcular ratings netos
    net_rating_a = calcular_net_rating(datos_a['Rating Ofensivo'], datos_a['Rating Defensivo'])
    net_rating_b = calcular_net_rating(datos_b['Rating Ofensivo'], datos_b['Rating Defensivo'])
    
    # Calcular probabilidades
    prob_a_decimal = predecir_probabilidad(net_rating_a, net_rating_b)
    prob_b_decimal = 1 - prob_a_decimal
    
    prob_a_porc = round(prob_a_decimal * 100, 1)
    prob_b_porc = round(prob_b_decimal * 100, 1)
    
    # Determinar favorito
    favorito = equipo_a if prob_a_porc > prob_b_porc else equipo_b
    favorito_prob = max(prob_a_porc, prob_b_porc)
    
    # Visualizar resultados con diseño mejorado
    col_prob_a, col_spacer, col_prob_b = st.columns([2, 1, 2])
    
    with col_prob_a:
        st.markdown(f"### {equipo_a}")
        st.markdown(f"<div style='text-align: center; padding: 2rem; background: {'#d4edda' if prob_a_porc > prob_b_porc else '#f8f9fa'}; border-radius: 10px; border: 3px solid {'#28a745' if prob_a_porc > prob_b_porc else '#dee2e6'};'>", unsafe_allow_html=True)
        st.metric(
            label="Probabilidad de Victoria",
            value=f"{prob_a_porc}%",
            delta=f"Net Rating: {net_rating_a:+.2f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_spacer:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### VS", unsafe_allow_html=True)
    
    with col_prob_b:
        st.markdown(f"### {equipo_b}")
        st.markdown(f"<div style='text-align: center; padding: 2rem; background: {'#d4edda' if prob_b_porc > prob_a_porc else '#f8f9fa'}; border-radius: 10px; border: 3px solid {'#28a745' if prob_b_porc > prob_a_porc else '#dee2e6'};'>", unsafe_allow_html=True)
        st.metric(
            label="Probabilidad de Victoria",
            value=f"{prob_b_porc}%",
            delta=f"Net Rating: {net_rating_b:+.2f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Barra de probabilidad visual
    st.markdown("### 📊 Visualización de Probabilidades")
    prob_diff = abs(prob_a_porc - prob_b_porc)
    
    if prob_diff < 5:
        st.warning("⚠️ **Encuentro muy parejo!** La diferencia es menor al 5%. Cualquier equipo puede ganar.")
    else:
        st.success(f"✅ **{favorito}** es el favorito con un {favorito_prob}% de probabilidad de victoria.")
    
    # Barra de progreso visual
    st.markdown(f"""
    <div style='background: #e9ecef; border-radius: 10px; padding: 1rem; margin: 1rem 0;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
            <span><strong>{equipo_a}</strong></span>
            <span><strong>{equipo_b}</strong></span>
        </div>
        <div style='display: flex; height: 30px; border-radius: 5px; overflow: hidden;'>
            <div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); width: {prob_a_porc}%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                {prob_a_porc}%
            </div>
            <div style='background: linear-gradient(90deg, #c82333 0%, #e74c3c 100%); width: {prob_b_porc}%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                {prob_b_porc}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Información adicional
    with st.expander("ℹ️ Sobre el Modelo de Predicción"):
        st.markdown(f"""
        **Metodología:**
        - Este modelo utiliza el **Rating Neto** (Rating Ofensivo - Rating Defensivo) para predecir resultados
        - La probabilidad se calcula usando una función logística que considera la diferencia entre los ratings
        - **{equipo_a}** tiene un Rating Neto de **{net_rating_a:+.2f}**
        - **{equipo_b}** tiene un Rating Neto de **{net_rating_b:+.2f}**
        
        **Limitaciones:**
        - Este es un modelo básico y no considera factores como lesiones, descanso, jugar en casa/visitante
        - Los resultados reales pueden variar significativamente
        - Úsalo como referencia, no como predicción garantizada
        """)


def main():
    """Función principal de la aplicación."""
    # El header se renderizará después de seleccionar los equipos
    
    # Obtener temporada seleccionada (temporal, antes de obtener datos)
    temporada_actual = obtener_temporada_actual()
    temporada_inicial = temporada_actual
    if not validar_temporada_disponible(temporada_actual):
        año_inicio = int(temporada_actual.split('-')[0])
        año_anterior = año_inicio - 1
        temporada_inicial = f"{año_anterior}-{str(año_inicio)[-2:]}"
    
    # Renderizar sidebar (sin datos aún para obtener selección de temporada)
    # Primero necesitamos obtener una temporada inicial para el sidebar
    temporadas_disponibles = generar_lista_temporadas(temporada_inicial, NUM_TEMPORADAS_RECIENTES)
    try:
        indice_default = temporadas_disponibles.index(temporada_inicial)
    except ValueError:
        indice_default = 0
    
    # Sidebar estilo betting
    st.sidebar.markdown("### ⚙️ CONFIG")
    
    # Badge de temporada estilo neon
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 0.75rem; background: #0f1422; border: 1px solid #00ff88; 
    border-radius: 8px; color: #00ff88; margin-bottom: 1rem;'>
        <div style='font-size: 0.7rem; color: #b4b4ff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.25rem;'>Temporada</div>
        <div style='font-size: 1.25rem; font-weight: 700; font-family: monospace;'>{temporada_inicial}</div>
    </div>
    """, unsafe_allow_html=True)
    
    temporada_seleccionada = st.sidebar.selectbox(
        "📅 TEMPORADA",
        temporadas_disponibles,
        index=indice_default,
        help="Selecciona la temporada a analizar"
    )
    
    st.sidebar.markdown("---")
    
    # Información de datos estilo compacto
    st.sidebar.markdown("""
    <div style='background: #0f1422; padding: 0.75rem; border-radius: 8px; border: 1px solid #1a2332;'>
        <div style='font-weight: 600; margin-bottom: 0.25rem; color: #00d9ff; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;'>Fuente</div>
        <div style='font-size: 0.7rem; color: #b4b4ff;'>
            API Oficial NBA<br/>stats.nba.com
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para forzar actualización estilo neon
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 ACTUALIZAR", use_container_width=True):
        obtener_datos_nba.clear()
        validar_temporada_disponible.clear()
        st.rerun()
    
    # Obtener datos con la temporada seleccionada
    df_nba_raw = obtener_datos_nba(temporada=temporada_seleccionada)
    
    if df_nba_raw.empty:
        st.error("❌ No se pudieron obtener los datos. Por favor, verifica tu conexión e intenta nuevamente.")
        st.stop()
    
    # Procesar datos
    df_nba = procesar_datos_nba(df_nba_raw)
    
    # Selección de equipos estilo betting
    st.sidebar.markdown("### 🏀 EQUIPOS")
    equipos_disponibles = sorted(df_nba['Equipo'].unique().tolist())
    
    equipo_a = st.sidebar.selectbox(
        "EQUIPO A",
        equipos_disponibles,
        index=equipos_disponibles.index(DEFAULT_TEAM_A) if DEFAULT_TEAM_A in equipos_disponibles else 0,
        help="Primer equipo"
    )
    
    st.sidebar.markdown("<div style='text-align: center; font-size: 1rem; margin: 0.5rem 0; color: #00d9ff; font-weight: 700; letter-spacing: 2px;'>VS</div>", unsafe_allow_html=True)
    
    default_index_b = equipos_disponibles.index(DEFAULT_TEAM_B) if DEFAULT_TEAM_B in equipos_disponibles else 1
    equipo_b = st.sidebar.selectbox(
        "EQUIPO B",
        equipos_disponibles,
        index=default_index_b,
        help="Segundo equipo"
    )
    
    # Filtrar datos de los equipos seleccionados
    datos_a = df_nba[df_nba['Equipo'] == equipo_a].iloc[0]
    datos_b = df_nba[df_nba['Equipo'] == equipo_b].iloc[0]
    
    # Renderizar header
    render_simple_header(equipo_a, equipo_b, temporada_seleccionada)
    
    # Calcular ratings netos y probabilidades para el Bento Grid
    net_rating_a = calcular_net_rating(datos_a['Rating Ofensivo'], datos_a['Rating Defensivo'])
    net_rating_b = calcular_net_rating(datos_b['Rating Ofensivo'], datos_b['Rating Defensivo'])
    prob_a = predecir_probabilidad(net_rating_a, net_rating_b)
    prob_b = 1 - prob_a
    
    # Renderizar Bento Grid con información clave
    render_bento_grid(datos_a, datos_b, equipo_a, equipo_b, net_rating_a, net_rating_b, prob_a, prob_b)
    
    # Preparar comparación
    comparacion_df = preparar_comparacion(datos_a, datos_b, equipo_a, equipo_b)
    
    # Renderizar tabs de comparación
    render_comparison_tabs(comparacion_df, equipo_a, equipo_b)
    
    # Renderizar sección de predicción (simplificada, ya está en Bento Grid)
    st.markdown("---")
    with st.expander("ℹ️ Información del Modelo de Predicción", expanded=False):
        st.markdown(f"""
        **Metodología:**
        - Modelo basado en **Rating Neto** (Rating Ofensivo - Rating Defensivo)
        - Función logística que considera la diferencia entre ratings
        - **{equipo_a}**: Rating Neto {net_rating_a:+.2f}
        - **{equipo_b}**: Rating Neto {net_rating_b:+.2f}
        
        **Limitaciones:**
        - No considera factores como lesiones, descanso, casa/visitante
        - Los resultados reales pueden variar significativamente
        - Úsalo como referencia estadística
        """)


if __name__ == "__main__":
    main()

