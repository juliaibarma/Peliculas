import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.data_loader import load_nulls


df = load_data()

st.title("🔎 EDA y Transformaciones de Datos")
st.markdown("""
En esta sección realizamos un **análisis exploratorio de datos (EDA)**, para conocer mejor el dataset y 
explicar las **transformaciones aplicadas durante la limpieza**.
""")

# Asegurar columnas derivadas (por si aún no están)
if "profit" not in df and {"gross","budget"}.issubset(df.columns):
    df["profit"] = df["gross"] - df["budget"]
if "roi" not in df and {"gross","budget"}.issubset(df.columns):
    df["roi"] = np.where(df["budget"]>0, (df["gross"]-df["budget"])/df["budget"], np.nan)

# =========================
# Filtros mínimos
# =========================
c1, c2 = st.columns(2)
# Años
if "year" in df:
    y_min, y_max = int(df["year"].min()), int(df["year"].max())
    years = c1.slider("Años", y_min, y_max, (y_min, y_max))
else:
    years = None
# Género
genres = sorted(df["genre"].dropna().unique().tolist()) if "genre" in df else []
sel_genres = c2.multiselect("Género", genres, default=[])

# Aplicar filtros
dff = df.copy()
if years and "year" in dff:
    dff = dff[dff["year"].between(years[0], years[1], inclusive="both")]
if sel_genres:
    dff = dff[dff["genre"].isin(sel_genres)]

# =========================
# 1) Distribuciones 
# =========================
st.subheader("📊 Distribuciones (numéricas y categóricas)")

left, right = st.columns(2)

# Numérica simple
with left:
    num_cols = [c for c in ["score","votes","budget","gross","runtime","profit","roi"] if c in dff]
    if num_cols:
        sel_num = st.selectbox("Variable numérica", num_cols, index=0, key="num1")
        fig = px.histogram(dff, x=sel_num, nbins=30, title=f"Distribución de {sel_num}")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Media: {dff[sel_num].mean():.2f} · Mediana: {dff[sel_num].median():.2f}")
    else:
        st.info("No hay variables numéricas disponibles.")

# Categórica simple (Top 10)
with right:
    cat_cols = [c for c in ["genre","country","company"] if c in dff]
    if cat_cols:
        sel_cat = st.selectbox("Variable categórica", cat_cols, index=0, key="cat1")
        vc = dff[sel_cat].value_counts().head(10).sort_values()
        fig = px.bar(x=vc.values, y=vc.index, orientation="h", title=f"{sel_cat} (Top 10)")
        fig.update_xaxes(title="Frecuencia"); fig.update_yaxes(title="")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Las categorías principales concentran la mayor parte del volumen.")
    else:
        st.info("No hay variables categóricas disponibles.")

# =========================
# 2) Evolución temporal
# =========================
st.subheader("⏳ Evolución temporal")
if "year" in dff:
    by_year = dff.groupby("year").size().reset_index(name="count")
    fig = px.line(by_year, x="year", y="count", markers=True, title="Películas por año")
    fig.update_yaxes(title="Nº de películas")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Crecimiento sostenido hasta ~2019; caída en 2020 (impacto pandemia).")
else:
    st.info("No hay columna 'year'.")

# =========================
# 3) Budget vs Gross 
# =========================
st.subheader("💰 Relación Budget vs Gross")
if {"budget","gross"}.issubset(dff.columns):
    fig = px.scatter(
        dff, x="budget", y="gross",
        color="genre" if "genre" in dff else None,
        hover_data=[c for c in ["name","year","company"] if c in dff],
        opacity=0.7, title="Budget vs Gross"
    )
    fig.update_xaxes(title="Budget", tickprefix="$", separatethousands=True)
    fig.update_yaxes(title="Gross", tickprefix="$", separatethousands=True)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Relación positiva con **mucha dispersión**: más presupuesto ↑ potencial, no garantiza taquilla.")
else:
    st.info("Faltan 'budget' o 'gross'.")

# =========================
# 4) Transformaciones 
# =========================
# Importar el CSV con % de nulos
st.subheader("🧹 Transformaciones y limpieza de datos")
nulls_df = load_nulls()

with st.expander("📊 % de valores nulos antes de limpiar", expanded=True):
    st.dataframe(nulls_df, use_container_width=True)
    st.caption("Porcentaje de valores nulos detectados antes del proceso de limpieza.")
    st.markdown("""
- **Columnas y tipos:** nombres normalizados; `score`, `votes`, `budget`, `gross`, `runtime`, `year` a numérico.
- **Nulos:**  
  - Numéricos (`gross`, `runtime`, `votes`, `score`) → **media**.  
  - Categóricos (`rating`, `company`, `country`, `writer`, `released`, `star`) → **\"Desconocido\"**.  
- **Budget:**  más del 20% de nulos → imputación con regresión lineal utilizando como predictores las variables year, votes, gross, runtime, rating y country.
- **Nuevas columnas:** `profit = gross - budget` y `roi = (gross - budget)/budget`.
""")

# =========================
# 5) Profit & ROI 
# =========================
st.subheader("📈 Profit & ROI")
if {"profit","roi","genre"}.issubset(dff.columns):
    cols = st.columns(2)

    # ROI por género (Top 10)
    with cols[0]:
        roi_gen = dff.groupby("genre")["roi"].mean().dropna().sort_values(ascending=False).head(10)
        fig = px.bar(x=roi_gen.values, y=roi_gen.index, orientation="h", title="ROI medio por género (Top 10)")
        fig.update_xaxes(title="ROI (x)")
        fig.update_yaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 por profit
    with cols[1]:
        top_profit = dff.sort_values("profit", ascending=False).head(10)
        fig = px.bar(top_profit, x="name", y="profit", title="Top 10 películas por profit")
        fig.update_yaxes(title="Profit", tickprefix="$", separatethousands=True)
        fig.update_xaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

    st.caption("El **ROI** mide eficiencia del presupuesto; el **profit** muestra beneficio absoluto.")
else:
    st.info("Se necesitan 'profit', 'roi' y 'genre' para esta sección.")