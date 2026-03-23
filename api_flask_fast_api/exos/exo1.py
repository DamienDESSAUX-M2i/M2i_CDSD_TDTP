from flask import Flask, jsonify

app = Flask(__name__)

HELLO_MAP = {
    "english": "Hello",
    "french": "Bonjour",
}


@app.route("/hello/<language>", methods=["GET"])
def hello(language):
    hello = HELLO_MAP.get(language, None)
    if hello is None:
        return jsonify(
            {
                "success": False,
                "error": f"Language not supported: language={list(HELLO_MAP.keys())}",
            }
        ), 400

    return jsonify({"success": True, "message": hello, "language": language}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
