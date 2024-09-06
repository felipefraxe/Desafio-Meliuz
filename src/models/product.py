import pandas as pd


def load_products(path="src/data/xpto_sales_products_mar_may_2024.csv"):
    """
    Carrega os dados de produtos do arquivo CSV especificado.
    
    :param path: Caminho para o arquivo CSV dos produtos.
    :return: DataFrame com os dados dos produtos.
    :raises FileNotFoundError: Se o arquivo CSV não for encontrado.
    :raises pd.errors.EmptyDataError: Se o arquivo CSV estiver vazio.
    :raises pd.errors.ParserError: Se houver um erro ao analisar o CSV.
    """

    try:
        return pd.read_csv(path, parse_dates=["sale_date"])
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo de dados de produtos não encontrado.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("Arquivo de dados de produtos está vazio.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Erro ao analisar o arquivo de dados de produtos.")


def load_recommended_data():
    """
    Manipula dados para com agregações úteis para algoritmo de recomendação
    """
    try:
        df = load_products()
        agg_df = df.groupby(["product_id"]).agg({
            "product_title": "first",
            "product_image_url": "first",
            "sales_per_day": lambda x: list(x.groupby(df["sale_date"].dt.to_period('M')).sum()),
            "product_price": "mean",
        }).reset_index()
        agg_df.rename(columns={ "sales_per_day": "sales_per_month" }, inplace=True)

        agg_df["total_revenue"] = agg_df["sales_per_month"].apply(sum) * agg_df["product_price"]

        min_price_info = df.loc[df.groupby("product_id")["product_price"].idxmin(), ["product_id", "product_price", "store_name", "store_id"]]
        agg_df = agg_df.drop(columns=["product_price"]).merge(min_price_info, on="product_id")

        return agg_df

    except Exception as err:
        raise err