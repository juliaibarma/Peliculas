import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def load_data(file_path = None):
    if file_path is None:
        data_path = Path(__file__).parent.parent / "data" / "movies_cleaned.csv"
    else:
        data_path = file_path

    df = pd.read_csv(data_path)
    if "year" in df.columns:
        df["year"] = df["year"].astype("int")

    return df

def load_nulls(file_path=None):
    if file_path is None:
        nulls_path = Path(__file__).parent.parent / "data" / "nulos.csv"
    else:
        nulls_path = file_path

    nulls_df = pd.read_csv(nulls_path)
    return nulls_df