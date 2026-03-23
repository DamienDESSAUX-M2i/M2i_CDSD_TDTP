from flask import Flask, jsonify, request

app = Flask(__name__)


def convert_c2f(c):
    return c * 9 / 5 + 32


def convert_f2c(f):
    return (f - 32) * 5 / 9


@app.route("/convert/temp", methods=["POST"])
def convert_temp():
    value = request.args.get("value", None)
    try:
        value = float(value)
    except Exception:
        return jsonify(
            {"success": False, "error": "Value must be an integer or a float"}
        ), 400

    unit = request.args.get("unit", None)
    match unit:
        case "c2f":
            return jsonify(
                {"success": True, "celsius": value, "fahrenheit": convert_f2c(value)}
            ), 200
        case "f2c":
            return jsonify(
                {"success": True, "fahrenheit": value, "celsius": convert_c2f(value)}
            ), 200
        case _:
            return jsonify(
                {"success": False, "error": "Unit not supported: unit=['c2f', 'f2c']"}
            ), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
