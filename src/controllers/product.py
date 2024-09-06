from flask import Blueprint, jsonify
import services.product

products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/recommend/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):
    try:
        return jsonify(services.product.fetch_top_k_recommended(5)), 200
    except Exception as err:
        return jsonify({"error": f"Erro interno do servidor: {str(err)}"}), 500