from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/calculate", methods=["POST"])
def convert_temp():
    a = request.args.get("a", None)
    b = request.args.get("b", None)
    try:
        a = float(a)
        b = float(b)
    except Exception:
        return jsonify(
            {"success": False, "error": "a and b must be an integer or a float"}
        ), 400

    operation = request.args.get("operation", None)
    match operation:
        case "add":
            return jsonify(
                {
                    "success": True,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": a + b,
                }
            ), 200
        case "subtract":
            return jsonify(
                {
                    "success": True,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": a - b,
                }
            ), 200
        case "multiply":
            return jsonify(
                {
                    "success": True,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": a * b,
                }
            ), 200
        case "divide":
            if b == 0:
                return jsonify(
                    {
                        "success": False,
                        "error": "Cannot divide by zero",
                    }
                ), 400
            return jsonify(
                {
                    "success": True,
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": a / b,
                }
            ), 200
        case _:
            return jsonify(
                {
                    "success": False,
                    "error": "Operation not supported: unit=['add', 'subtract', 'multiply', 'divide']",
                }
            ), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
