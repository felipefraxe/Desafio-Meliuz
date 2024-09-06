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
