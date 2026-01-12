import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_loader import load_data


df = load_data()

st.title("📙 Resultados y conclusiones")
st.markdown("Resumen con *KPIs, evolución de **ROI, **eficiencia por género* y *películas destacadas*.")

# ===== KPIs (fila superior, claros y suficientes) =====
c1, c2, c3, c4 = st.columns(4)
c1.metric("🎞 Películas", f"{len(df):,}")
c2.metric("📈 ROI medio", f"{df['roi'].mean():.2f}x" if 'roi' in df else "—")
c3.metric("💰 Profit medio", f"${df['profit'].mean():,.0f}" if 'profit' in df else "—")
if {"genre","roi"}.issubset(df.columns) and df["roi"].notna().any():
    best_genre = df.groupby("genre")["roi"].mean().idxmax()
else:
    best_genre = "—"
c4.metric("🥇 Género más rentable", best_genre)

st.markdown("---")

# ===== ROI por década (mediana recortada) + volumen por década =====
st.subheader("⏳ Evolución de la rentabilidad por década")

# Asegura decade
if "decade" not in df.columns and "year" in df.columns:
    df["decade"] = (df["year"] // 10) * 10

col1, col2 = st.columns((2,1))

with col1:
    if {"decade","roi"}.issubset(df.columns):
        # Limitar extremos para una lectura realista
        limit = st.checkbox("Limitar ROI a 0–100", value=True)
        dtemp = df[df["roi"].notna()].copy()
        if limit:
            dtemp = dtemp[dtemp["roi"].between(0, 100, inclusive="both")]

        # Mediana (robusta a outliers)
        roi_decade = (
            dtemp.groupby("decade")["roi"]
            .median()
            .reset_index(name="roi_mediana")
            .sort_values("decade")
        )

        # Si no hay datos suficientes, avisamos
        if roi_decade.empty:
            st.info("No hay datos suficientes para calcular el ROI por década.")
        else:
            fig = px.line(
                roi_decade, x="decade", y="roi_mediana",
                markers=True, title="ROI mediano por década (sin extremos)"
            )
            fig.update_xaxes(title="Década")
            fig.update_yaxes(title="ROI mediano (x)")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Usamos *mediana* y recorte de extremos para evitar que un caso atípico distorsione la lectura.")
    else:
        st.info("No hay columnas suficientes para ROI por década.")

with col2:
    if "decade" in df.columns:
        count_decade = df.groupby("decade").size().reset_index(name="películas")
        fig_cnt = px.bar(count_decade, x="decade", y="películas", title="Nº de películas por década")
        fig_cnt.update_yaxes(separatethousands=True)
        st.plotly_chart(fig_cnt, use_container_width=True)
        st.caption("Volumen de títulos por década para contextualizar la evolución del ROI.")
    else:
        st.info("No hay columna 'decade' para mostrar volumen por década.")

st.markdown("---")

# ===== ROI por género =====
st.subheader("🎭 ROI medio por género")
if {"genre","roi"}.issubset(df.columns):
    roi_gen = (
        df[df["roi"].between(0, 100, inclusive="both")]  # recorte suave para que no ‘estire’ el eje
        .groupby("genre")["roi"].mean()
        .dropna()
        .sort_values(ascending=False)
        .head(12)
        .sort_values(ascending=True)
    )
    fig = px.bar(
        x=roi_gen.values, y=roi_gen.index, orientation="h",
        title="Géneros con mejor ROI medio", text=roi_gen.values
    )
    fig.update_traces(texttemplate="%{text:.2f}x", textposition="outside")
    fig.update_xaxes(title="ROI (x)")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Faltan 'genre' y/o 'roi' para este gráfico.")