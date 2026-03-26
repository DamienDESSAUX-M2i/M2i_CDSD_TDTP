
from flask import Blueprint, jsonify, request

bp = Blueprint('converter', __name__)


@bp.route('/convert/temp', methods=['GET'])
def convert_temperature():
    try:
        value_str = request.args.get('value')
        unit = request.args.get('unit', '').lower()

        if not value_str:
            return jsonify({'error': 'Missing parameter: value'}), 400
        if not unit:
            return jsonify({'error': 'Missing parameter: unit'}), 400

        try:
            value = float(value_str)
        except ValueError:
            return jsonify({
                'error': 'Value must be a valid number',
                'received': value_str
            }), 400

        if unit == 'c2f':
            fahrenheit = value * 9/5 + 32
            result = {'celsius': value, 'fahrenheit': round(fahrenheit, 2)}
        elif unit == 'f2c':
            celsius = (value - 32) * 5/9
            result = {'fahrenheit': value, 'celsius': round(celsius, 2)}
        else:
            return jsonify({
                'error': 'Unit must be c2f or f2c',
                'received': unit
            }), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
