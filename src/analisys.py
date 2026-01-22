import pandas as pd

def set_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["Satisfacao_Alta"] = df["Quality of Recent Support (Rating)"].apply(lambda x: 1 if x >= 4 else 0)
    # SLA baseado em 60s conforme padrão ITIL
    df["SLA"] = df["First Response Time (seconds)"].apply(lambda x: 1 if x <= 60 else 0)
    return df


# Retorna os números finais para os Cards do Dashboard
def calculate_kpis(df: pd.DataFrame):
    tma_resposta = df["First Response Time (seconds)"].mean()
    tma_medio = df["Call Handle Time (minutes)"].mean()
    fcr_rate = (df["FCR"].mean()) * 100    
    sla_compliance = (df['SLA'].mean()) * 100
    return tma_resposta, tma_medio, fcr_rate, sla_compliance


def insights(df: pd.DataFrame):
    custo_por_topico = df.groupby("Customer Inquiry Topic")["Fully Burdened Cost per call"].mean().sort_values(ascending=False)
    ranking_agentes = df.groupby('Agent ID/Name')['Quality of Recent Support (Rating)'].mean().sort_values(ascending=False)
    return custo_por_topico, ranking_agentes