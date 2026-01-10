# 🏀 Análisis de Datos NBA

Aplicación web interactiva para análisis y comparación de estadísticas de equipos de la NBA, construida con Streamlit.

## 📋 Características

- 📊 **Análisis en tiempo real**: Datos actualizados desde la API oficial de la NBA
- 🔄 **Detección automática de temporada**: Selecciona automáticamente la temporada más reciente disponible
- 📈 **Visualizaciones interactivas**: Gráficos dinámicos con Plotly
- 🤖 **Modelo de predicción**: Predicción de probabilidades de victoria basada en ratings netos
- 🎯 **Comparación de equipos**: Comparación detallada entre dos equipos

## 🏗️ Estructura del Proyecto

```
AnalisisNBA/
├── app.py                 # Archivo principal de Streamlit
├── config.py              # Configuración y constantes
├── requirements.txt       # Dependencias del proyecto
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── season_utils.py   # Funciones para manejo de temporadas
│   ├── nba_api.py        # Conexión a la API de NBA
│   └── data_processing.py # Procesamiento de datos
├── analysis/              # Módulos de análisis
│   ├── __init__.py
│   ├── predictions.py    # Modelos de predicción
│   └── visualizations.py # Funciones de visualización
└── venv/                  # Entorno virtual
```

## 🚀 Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## ▶️ Uso

Ejecutar la aplicación:
```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📦 Dependencias

- `streamlit` - Framework para aplicaciones web
- `pandas` - Análisis de datos
- `plotly` - Visualizaciones interactivas
- `numpy` - Cálculos numéricos
- `requests` - Solicitudes HTTP
- `nba-api` - Cliente para la API de NBA

## 🔧 Configuración

Las configuraciones principales se encuentran en `config.py`:
- URLs y parámetros de la API
- Timeouts y reintentos
- Mapeo de columnas
- Equipos por defecto

## 📝 Notas

- Los datos se actualizan automáticamente cada hora
- La aplicación intenta usar primero `requests` directo, y si falla, usa `nba-api` como respaldo
- Los datos provienen de la API oficial de stats.nba.com

## 📄 Licencia

Este proyecto es de código abierto.

