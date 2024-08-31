import pandas as pd


def load_produtcs(path="src/data/xpto_sales_products_mar_may_2024.csv"):
    return pd.read_csv(path, index_col="product_id")