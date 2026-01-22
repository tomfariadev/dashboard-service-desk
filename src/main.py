import pandas as pd
import streamlit as st
import os
import data_cleaning as dc
import analisys as ana
import graphics as gf

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "..", "data", "service_ops_performance_data.csv")
print(file_path)

@st.cache_data
def get_data():
    raw_data = pd.read_csv(file_path)
    clean_data = dc.cleaning(raw_data)
    return ana.set_metrics(clean_data)

def main():
    df = get_data()
    gf.generate_grafic(df)

if __name__ == "__main__":
    main()