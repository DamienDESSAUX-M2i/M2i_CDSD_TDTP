from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)

model_name = "papluca/xlm-roberta-base-language-detection"
detector = pipeline("text-classification", model=model_name)


def validate_text(text: str) -> tuple[bool, str]:
    if not isinstance(text, str):
        return False, "Text must be a string"

    if text.strip() == "":
        return False, "Text empty"

    if len(text) > 500:
        return False, "Length of text must be less than 500 characters"

    return True, "Text valid"


def validate_texts(texts: list[str]) -> tuple[bool, str]:
    if not isinstance(texts, list):
        return False, "Texts must be a list"

    if len(texts) == 0:
        return False, "Texts empty"

    if len(texts) > 100:
        return False, "Too many texts (max 100)"

    if not all(validate_text(text)[0] for text in texts):
        return False, "Each text must be non-empty and <= 500 chars"

    return True, "Texts valid"


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "model": "papluca/xlm-roberta-base-language-detection",
        }
    )


@app.route("/detect", methods=["POST"])
def detect():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json()

    if data.get("text") is None:
        return jsonify({"error": "Field missing: text"}), 400

    text = data["text"]

    text_is_valid, message = validate_text(text)
    if not text_is_valid:
        return jsonify({"error": message}), 400

    result = detector(text)[0]

    return jsonify(
        {
            "text": text,
            "language": result["label"],
            "confidence": result["score"],
        }
    ), 200


@app.route("/detect/batch", methods=["POST"])
def detect_batch():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json()

    if data.get("texts") is None:
        return jsonify({"error": "Field missing: texts"}), 400

    texts = data["texts"]

    texts_is_valid, message = validate_texts(texts)
    if not texts_is_valid:
        return jsonify({"error": message}), 400

    results = detector(texts)

    return jsonify(
        {
            "data": [
                {
                    "text": text,
                    "language": result["label"],
                    "confidence": result["score"],
                }
                for text, result in zip(texts, results)
            ]
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
