# 🎥 Análisis de la Industria del Cine

Este proyecto explora la evolución de la industria cinematográfica a través de un análisis de datos, utilizando herramientas interactivas para visualizar tendencias, métricas clave y transformaciones en el sector.

## 🚀 Descripción

El objetivo principal es analizar datos relacionados con películas, incluyendo presupuestos, ingresos, géneros y más, para responder preguntas como:
- ¿Qué géneros son más rentables?
- ¿Cómo ha evolucionado la rentabilidad a lo largo de las décadas?
- ¿Qué factores impulsan el éxito de una película?

El análisis se presenta mediante una aplicación interactiva desarrollada con **Streamlit**, que incluye:
- **Inicio**: Introducción al análisis.
- **EDA**: Exploración de datos y transformaciones.
- **Conclusiones**: Resultados clave y métricas destacadas.

## 📂 Estructura del Proyecto

- **`app.py`**: Archivo principal para ejecutar la aplicación.
- **`data/`**: Contiene los datasets procesados (`movies_cleaned.csv`, `nulos.csv`).
- **`ui/`**: Componentes de la interfaz de usuario:
  - `inicio.py`: Página de introducción.
  - `eda.py`: Análisis exploratorio de datos.
  - `conclusiones.py`: Resultados y conclusiones.
- **`utils/`**: Funciones auxiliares:
  - `config.py`: Configuración de la aplicación.
  - `data_loader.py`: Carga y procesamiento de datos.

## 🛠️ Tecnologías

- **Python**: Lenguaje principal.
- **Streamlit**: Framework para aplicaciones web interactivas.
- **Pandas**: Manipulación y análisis de datos.
- **Plotly**: Visualización de datos.

## 📊 Visualizaciones

- **KPIs generales**: Métricas clave como ROI, profit medio, y género más rentable.
- **Evolución temporal**: Rentabilidad por década.
- **Distribuciones**: Análisis de variables numéricas y categóricas.

## 📦 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/Peliculas.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## 📄 Dataset

El análisis utiliza datos de [Kaggle: Movies Dataset](https://www.kaggle.com/datasets/danielgrijalvas/movies).

## ✨ Demo

Explora la aplicación interactiva para obtener insights clave sobre la industria del cine.

