from flask import Flask, redirect, url_for
from controllers.product import products_bp

app = Flask(__name__)

app.register_blueprint(products_bp)

@app.route("/")
def hello_world():
    return redirect(url_for("get_recommendations", user_id=1))

@app.route("/recommend/<int:user_id>")
def get_recommendations(user_id):
    return f"<p>Recommendations for user {user_id}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)