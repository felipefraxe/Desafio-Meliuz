from models.product import load_produtcs

def fetch_products():
    return load_produtcs().head(5)
