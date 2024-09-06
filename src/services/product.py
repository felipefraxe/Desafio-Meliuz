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
        df = models.product.load_recommended_data()        

        df["sales_slope"] = df["sales_per_month"].apply(calculate_sales_slope)
        
        df = df[df["sales_slope"] > 0]
        df = df[df["sales_slope"] >= df["sales_slope"].quantile(0.25)]

        growing_products = df.sort_values(by="total_revenue", ascending=False)

        growing_products.drop(columns=["sales_per_month", "sales_slope", "total_revenue"], inplace=True)

        return growing_products.head(k).to_dict(orient="records")

    except Exception as err:
        raise err
