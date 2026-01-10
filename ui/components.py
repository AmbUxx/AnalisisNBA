"""
Componentes UI reutilizables para la aplicación - Estilo Betting/Fintech
"""

import streamlit as st
import pandas as pd


def render_comparison_table(comparacion_df, equipo_a, equipo_b):
    """
    Renderiza una tabla de comparación estilo betting - compacta y high-density.
    
    Args:
        comparacion_df (pd.DataFrame): DataFrame con datos de comparación
        equipo_a (str): Nombre del equipo A
        equipo_b (str): Nombre del equipo B
        
    Returns:
        None
    """
    # Categorizar métricas según prioridad para betting
    categorias = {
        "🎯 Probabilidades Clave": ["Porc. Victoria"],
        "⚡ Eficiencia Ofensiva": ["Rating Ofensivo", "Asistencias"],
        "🛡️ Eficiencia Defensiva": ["Rating Defensivo", "Pérdidas"],
        "🏃 Ritmo de Juego": ["Ritmo de Juego"],
        "📊 Stats de Creación": ["AST/TO", "3P%"]
    }
    
    # comparacion_df tiene estructura: índice=métricas, columnas=equipos
    # No necesitamos transponer, trabajamos directamente con comparacion_df
    
    # Renderizar cada categoría
    for categoria, metricas in categorias.items():
        # Filtrar métricas que existen en el DataFrame
        metricas_disponibles = [m for m in metricas if m in comparacion_df.index]
        
        if not metricas_disponibles:
            continue
        
        st.markdown(f"### {categoria}")
        
        # Crear sub-dataframe con las métricas de esta categoría
        df_categoria = comparacion_df.loc[metricas_disponibles]
        
        # Crear lista de datos para el DataFrame con información de mejor/peor
        filas = []
        datos_auxiliares = []  # Guardar información adicional para estilos
        
        for idx in metricas_disponibles:
            valor_a = df_categoria.loc[idx, equipo_a]
            valor_b = df_categoria.loc[idx, equipo_b]
            
            # Determinar mejor y peor
            if 'Defensivo' in idx or 'Pérdidas' in idx:
                es_mejor_a = valor_a < valor_b
            else:
                es_mejor_a = valor_a > valor_b
            
            # Formatear valores
            if '%' in idx or 'Porc' in idx:
                valor_a_str = f"{valor_a:.1%}"
                valor_b_str = f"{valor_b:.1%}"
            elif 'Rating' in idx:
                valor_a_str = f"{valor_a:.2f}"
                valor_b_str = f"{valor_b:.2f}"
            else:
                valor_a_str = f"{valor_a:.2f}"
                valor_b_str = f"{valor_b:.2f}"
            
            # Representación clara del mejor equipo usando nombres
            # Extraer nombre corto del equipo (primera palabra o abreviación)
            def obtener_nombre_corto(nombre_completo):
                """Obtiene un nombre corto del equipo"""
                palabras = nombre_completo.split()
                if len(palabras) > 1:
                    # Si tiene múltiples palabras, usar la primera
                    return palabras[0]
                else:
                    # Si es una sola palabra, usar primeros 8 caracteres
                    return nombre_completo[:8]
            
            nombre_a_corto = obtener_nombre_corto(equipo_a)
            nombre_b_corto = obtener_nombre_corto(equipo_b)
            
            # Formato más claro: nombre del equipo con flecha direccional
            if es_mejor_a:
                mejor_str = f"◄ {nombre_a_corto}"  # Equipo A es mejor (flecha apunta a la izquierda)
            else:
                mejor_str = f"{nombre_b_corto} ►"  # Equipo B es mejor (flecha apunta a la derecha)
            
            filas.append({
                'Métrica': idx,
                equipo_a: valor_a_str,
                equipo_b: valor_b_str,
                'Mejor': mejor_str
            })
            
            # Guardar datos auxiliares
            datos_auxiliares.append({
                'es_mejor_a': es_mejor_a,
                'valor_a': valor_a,
                'valor_b': valor_b
            })
        
        df_display = pd.DataFrame(filas)
        
        # Función para aplicar estilos por fila
        def aplicar_estilos(row):
            """Aplica estilos: verde para mejor, rojo para peor"""
            fila_idx = row.name
            aux_data = datos_auxiliares[fila_idx]
            es_mejor_a = aux_data['es_mejor_a']
            
            # Crear array de estilos para cada columna
            estilos = [''] * len(row)
            columnas = list(row.index)
            
            # Índices de columnas
            idx_metrica = columnas.index('Métrica')
            idx_equipo_a = columnas.index(equipo_a)
            idx_equipo_b = columnas.index(equipo_b)
            idx_mejor = columnas.index('Mejor')
            
            # Estilo para columna "Mejor" - cian
            estilos[idx_mejor] = 'color: #00d9ff; font-weight: 700; text-align: center; font-family: monospace; font-size: 1rem;'
            
            # Aplicar estilos según cuál es mejor
            if es_mejor_a:
                # Equipo A es mejor - verde
                estilos[idx_equipo_a] = 'background-color: rgba(0, 255, 136, 0.25); color: #00ff88; font-weight: 700; font-family: monospace; border-left: 3px solid #00ff88; padding-left: 0.5rem;'
                # Equipo B es peor - rojo
                estilos[idx_equipo_b] = 'background-color: rgba(255, 68, 68, 0.25); color: #ff4444; font-weight: 600; font-family: monospace;'
            else:
                # Equipo B es mejor - verde
                estilos[idx_equipo_b] = 'background-color: rgba(0, 255, 136, 0.25); color: #00ff88; font-weight: 700; font-family: monospace; border-left: 3px solid #00ff88; padding-left: 0.5rem;'
                # Equipo A es peor - rojo
                estilos[idx_equipo_a] = 'background-color: rgba(255, 68, 68, 0.25); color: #ff4444; font-weight: 600; font-family: monospace;'
            
            return estilos
        
        # Aplicar estilos
        try:
            df_styled = df_display.style.apply(aplicar_estilos, axis=1)
        except Exception as e:
            st.error(f"Error en estilos: {e}")
            df_styled = df_display
        
        # Mostrar tabla
        st.dataframe(
            df_styled,
            use_container_width=True,
            hide_index=True
        )


def render_simple_header(equipo_a, equipo_b, temporada):
    """
    Renderiza un header estilo betting - compacto y funcional.
    """
    st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #00ff88; margin-bottom: 1.5rem;'>
            <h1 style='color: #00ff88; margin: 0; font-size: 2rem; font-weight: 700; letter-spacing: 1px; font-family: monospace;'>
                {equipo_a} <span style='color: #00d9ff; font-weight: 300;'>VS</span> {equipo_b}
            </h1>
            <p style='color: #b4b4ff; margin: 0.5rem 0 0 0; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;'>
                Temporada {temporada}
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_bento_grid(datos_a, datos_b, equipo_a, equipo_b, net_rating_a, net_rating_b, prob_a, prob_b):
    """
    Renderiza un layout Bento Grid con información clave para betting.
    
    Args:
        datos_a, datos_b: Series con datos de equipos
        equipo_a, equipo_b: Nombres de equipos
        net_rating_a, net_rating_b: Ratings netos
        prob_a, prob_b: Probabilidades de victoria
    """
    # Bloque Principal: Probabilidades y Win Probability
    col_main_1, col_main_2 = st.columns([2, 1])
    
    with col_main_1:
        st.markdown("### 🎯 Win Probability")
        prob_a_pct = round(prob_a * 100, 1)
        prob_b_pct = round(prob_b * 100, 1)
        
        # Barra de probabilidad visual
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.75rem; color: #b4b4ff;'>
                <span><strong>{equipo_a}</strong></span>
                <span><strong>{equipo_b}</strong></span>
            </div>
            <div style='display: flex; height: 40px; border-radius: 6px; overflow: hidden; background: #1a2332;'>
                <div style='background: linear-gradient(90deg, #00ff88 0%, #00d9ff 100%); width: {prob_a_pct}%; display: flex; align-items: center; justify-content: center; color: #0a0e27; font-weight: 700; font-family: monospace; font-size: 1.1rem;'>
                    {prob_a_pct}%
                </div>
                <div style='background: linear-gradient(90deg, #ff4444 0%, #ff8c00 100%); width: {prob_b_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-family: monospace; font-size: 1.1rem;'>
                    {prob_b_pct}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_main_2:
        st.markdown("### 📊 Net Rating")
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 1rem;'>
            <div style='margin-bottom: 0.75rem;'>
                <div style='color: #b4b4ff; font-size: 0.75rem; margin-bottom: 0.25rem;'>{equipo_a}</div>
                <div style='color: #00ff88; font-family: monospace; font-size: 1.5rem; font-weight: 700;'>{net_rating_a:+.2f}</div>
            </div>
            <div>
                <div style='color: #b4b4ff; font-size: 0.75rem; margin-bottom: 0.25rem;'>{equipo_b}</div>
                <div style='color: #ff4444; font-family: monospace; font-size: 1.5rem; font-weight: 700;'>{net_rating_b:+.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bloque Secundario: Stats Clave Compactas
    st.markdown("---")
    st.markdown("### 📈 Key Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 0.75rem; text-align: center;'>
            <div style='color: #b4b4ff; font-size: 0.7rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;'>Win Rate</div>
            <div style='color: #00ff88; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_a['Porc. Victoria']:.1%}</div>
            <div style='color: #ff4444; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_b['Porc. Victoria']:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 0.75rem; text-align: center;'>
            <div style='color: #b4b4ff; font-size: 0.7rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;'>OFF Rating</div>
            <div style='color: #00ff88; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_a['Rating Ofensivo']:.1f}</div>
            <div style='color: #ff4444; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_b['Rating Ofensivo']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 0.75rem; text-align: center;'>
            <div style='color: #b4b4ff; font-size: 0.7rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;'>DEF Rating</div>
            <div style='color: #ff4444; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_a['Rating Defensivo']:.1f}</div>
            <div style='color: #00ff88; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_b['Rating Defensivo']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: #0f1422; border: 1px solid #1a2332; border-radius: 8px; padding: 0.75rem; text-align: center;'>
            <div style='color: #b4b4ff; font-size: 0.7rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;'>PACE</div>
            <div style='color: #00d9ff; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_a['Ritmo de Juego']:.1f}</div>
            <div style='color: #00d9ff; font-family: monospace; font-size: 1.25rem; font-weight: 700;'>{datos_b['Ritmo de Juego']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)


def render_metric_card(label, value, delta=None, delta_color="normal"):
    """
    Renderiza una tarjeta de métrica estilo betting.
    
    Args:
        label (str): Etiqueta de la métrica
        value (str): Valor principal
        delta (str): Valor delta (opcional)
        delta_color (str): Color del delta ("normal", "inverse")
    """
    st.metric(label=label, value=value, delta=delta)
