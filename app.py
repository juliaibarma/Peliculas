import streamlit as st
from utils.config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)
#st.title("🎬 Análisis sobre la industria del cine")

pages = {
    "pages": [
        st.Page("ui/inicio.py", title="Inicio"),
        st.Page("ui/eda.py", title="EDA"),
        st.Page("ui/conclusiones.py", title="Conclusiones"),
    ],
}
pg = st.navigation(pages, position="hidden")

with st.sidebar:
    st.markdown("### Navegación")
    # Links de páginas
    st.page_link("ui/inicio.py", label="Inicio", icon="🏠")
    st.page_link("ui/eda.py", label="EDA", icon="📊")
    st.page_link("ui/conclusiones.py", label="Conclusiones", icon="📙")

    st.markdown("---")
    st.markdown("### Recursos")
    # Links de recursos externos
    st.page_link("https://www.kaggle.com/datasets/danielgrijalvas/movies", label="Dataset original", icon="💿")

pg.run()
