from flask import Blueprint, jsonify
from services.product import fetch_products

products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/recomendacao/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):
    print(user_id)
    produtos_recomendados = fetch_products()
    return jsonify(produtos_recomendados.to_dict(orient="records"))