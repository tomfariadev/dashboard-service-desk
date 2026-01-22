import pandas as pd
import streamlit as st
import plotly.express as px
import analisys as ana

# Configurações

def generate_grafic(df: pd.DataFrame):
    st.set_page_config(page_title = "Dashboard", layout = "wide")
    st.title("Indicadores de Performance para Service Desk")
    
    # sidebar
    st.sidebar.header("Filtros")
    
    topico = st.sidebar.multiselect(
        "Tópicos",
        options = df["Customer Inquiry Topic"].unique(),
        default = df['Customer Inquiry Topic'].unique()
    )

    meses_disponiveis = sorted(df["mes_nome"].unique())
    meses_selecionados = st.sidebar.multiselect(
        "Mês",
        options = meses_disponiveis,
        default = meses_disponiveis
    )

    # Filtros sidebar
    df_filtered = df[
        (df["Customer Inquiry Topic"].isin(topico)) &
        (df["mes_nome"].isin(meses_selecionados))
    ]

    tma_resposta, tma_medio, fcr, sla = ana.calculate_kpis(df_filtered)

    # l - Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        #tma = df_filtered['Call Handle Time (minutes)'].mean()
        st.metric("TMA Médio", f"{tma_medio:.2f} min")

    with col2:
        #fcr = (df_filtered['FCR'].mean()) * 100
        st.metric("Taxa de FCR", f"{fcr:.1f}%")

    with col3:
        st.metric("Compliance SLA", f"{sla:.1f}%")
    
    with col4:
        custo_total = df_filtered['Fully Burdened Cost per call'].sum()
        st.metric("Custo Total da Operação", f"R$ {custo_total:,.2f}")

    # 2 - Grafico
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Evolução do Custo por Tópico")
        fig_custo = px.bar(
            df_filtered.groupby("Customer Inquiry Topic")["Fully Burdened Cost per call"].sum().reset_index(), 
            x = "Customer Inquiry Topic", 
            y = "Fully Burdened Cost per call",
            color = "Customer Inquiry Topic",
            labels={
                'Customer Inquiry Topic': 'Tópico do Atendimento',
                'Fully Burdened Cost per call': 'Custo Total (R$)'
            },
            title="Custo Total por Categoria de Chamado"
        )
        st.plotly_chart(fig_custo, use_container_width=True)

    with c2:
        st.subheader("Satisfação por Agente")
        fig_sat = px.box(
            df_filtered, 
            x = "Agent ID/Name",
            y = "Quality of Recent Support (Rating)",
            color = "Agent ID/Name",
            labels = {
                "Agent ID/Name": "Agent",
                "Quality of Recent Support (Rating)": "Rating"
            }
        )
        st.plotly_chart(fig_sat, use_container_width=True)