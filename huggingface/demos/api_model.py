from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "model": "distilbert-base-uncased-finetuned-sst-2-english",
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", None)
    if text is None:
        return jsonify({"error": "Empty text"}), 400
    result = classifier(text)[0]
    return jsonify(
        {
            "text": text,
            "label": result["label"],
            "score": result["score"],
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
