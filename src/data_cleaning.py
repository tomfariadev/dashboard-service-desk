import pandas as pd 

def cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df["Time"] = pd.to_timedelta(df["Time"])
    df["Date"] = pd.to_datetime(df["Date"])
    
    df["mes"] = df["Date"].dt.month
    meses_desc = {1:"Jan",
                  2:"Fev",
                  3:"Mar",
                  4:"Abr",
                  5:"Mai",
                  6:"Jun",
                  7:"Jul",
                  8:"Ago",
                  9:"Set",
                  10:"Out",
                  11:"Nov",
                  12:"Dez"
                }
    df["mes_nome"] = df["mes"].map(meses_desc)

    df["dia_semana"] = df["Date"].dt.day_name

    # conversão de categorias (FCR: Yes/No -> 1/0)
    df["FCR"] = df["First Call Resolution (FCR) (Yes/No)"].map({"Yes": 1, "No": 0})
    
    # conversao do campo Customer Retention (Yes/No)
    df["Customer_Retention"] = df["Customer Retention (Yes/No)"].map({"Yes": 1, "No": 0})

    return df