import models.product
from sklearn.linear_model import LinearRegression
import numpy as np


def calculate_sales_slope(sales):
    """
    Calculates the slope of a linear regression fitted to the sales data over months.
    
    :param sales_list: List of sales per month.
    :return: Slope of the fitted regression line.
    """
    if len(sales) != 3:
        return 0

    months = np.array([1, 2, 3]).reshape(-1, 1)
    reg = LinearRegression().fit(months, sales)
    
    return reg.coef_[0]


def fetch_top_k_recommended(k=5):
    """
    Carrega os dados de produtos e aplica a lógica de recomendação.

    :return: DataFrame com os produtos processados.
    """
    try:
        df = models.product.load_products()
        agg_df = df.groupby(["product_id"]).agg({
            "product_title": "first",
            "product_image_url": "first",
            "sales_per_day": lambda x: list(x.groupby(df["sale_date"].dt.to_period('M')).sum()),
            "product_price": "mean",
        }).reset_index()
        agg_df.rename(columns={ "sales_per_day": "sales_per_month" }, inplace=True)

        agg_df["sales_slope"] = agg_df["sales_per_month"].apply(calculate_sales_slope)
        
        agg_df = agg_df[agg_df["sales_slope"] > 0]
        agg_df = agg_df[agg_df["sales_slope"] >= agg_df["sales_slope"].quantile(0.25)]

        agg_df["total_revenue"] = agg_df["sales_per_month"].apply(sum) * agg_df["product_price"]

        growing_products = agg_df.sort_values(by="total_revenue", ascending=False)

        min_price_info = df.loc[df.groupby("product_id")["product_price"].idxmin(), ["product_id", "product_price", "store_name", "store_id"]]
        growing_products = growing_products \
            .drop(columns=["product_price", "total_revenue", "sales_slope", "sales_per_month"]) \
            .merge(min_price_info, on="product_id")

        return growing_products.head(k).to_dict(orient="records")

    except Exception as err:
        raise err
