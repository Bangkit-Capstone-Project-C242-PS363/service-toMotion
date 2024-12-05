from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from tomotion import tomotion

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the API"})


@app.route("/tomotion", methods=["POST"])
def submit():
    data = request.json["data"]
    to_motion = tomotion(data)
    return jsonify({"error": False, "message": "Data received", "url": to_motion})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "status": 404}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

