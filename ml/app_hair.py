from flask import Flask, request, jsonify
from pipeline import predict

app = Flask(__name__)

@app.route("/infer", methods=["POST"])
def infer():
    features = request.json.get("features")
    y = predict(features)
    return jsonify({"prediction": y})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
