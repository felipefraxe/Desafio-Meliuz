from flask import Flask
from controllers.product import products_bp

app = Flask(__name__)

app.register_blueprint(products_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)