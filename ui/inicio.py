import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data


df = load_data()

st.title("🎬 Análisis sobre la industria del cine")

st.markdown(
    "**El cine ha vivido una transformación radical en las últimas décadas.**\n\n"
    "Desde los grandes estrenos en salas hasta el auge del streaming, "
    "la forma en que consumimos películas y el tipo de producciones que triunfan han cambiado enormemente. "
    "Pero, ¿es la aparición de las plataformas digitales la única responsable de estos cambios? "
    "Aquí exploramos datos clave sobre taquilla, presupuestos, géneros, valoraciones y talentos ✨, "
    "para entender cómo ha evolucionado la industria y qué factores impulsan el éxito o el fracaso de una película.\n\n"
    "📌 **Nota:** este análisis está centrado en las producciones de la gran pantalla 🎥, "
    "sin incluir contenidos de plataformas digitales."
)

# ====== Selector ======
option = st.selectbox(
    "Selecciona qué quieres visualizar 👇",
    ("KPIs generales", "Top 5 películas"),
)
# ====== KPIs ======
if option == "KPIs generales":
    n_movies = len(df)
    years_range = (int(df["year"].min()), int(df["year"].max()))
    n_genres = df["genre"].nunique()
    avg_budget = df["budget"].mean()
    avg_gross = df["gross"].mean()
    avg_roi = df["roi"].mean()
    avg_score = df["score"].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("🎞️ Nº de películas", f"{n_movies:,}")
    c2.metric("📅 Rango de años", f"{years_range[0]}–{years_range[1]}")
    c3.metric("🎭 Nº de géneros", f"{n_genres}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💵 Budget medio", f"${avg_budget:,.0f}")
    c2.metric("💰 Gross medio", f"${avg_gross:,.0f}")
    c3.metric("📈 ROI medio", f"{avg_roi:.2f}x")
    c4.metric("⭐ Score medio", f"{avg_score:.1f}")

# ====== Top 5 películas ======
elif option == "Top 5 películas":
    top5 = df.sort_values("gross", ascending=False).head(5)
    fig = px.bar(
        top5,
        x="name",
        y="gross",
        text="gross",
        color="name",
        title="Top 5 películas por recaudación",
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Recaudación (Gross)")

    st.plotly_chart(fig, use_container_width=True)


