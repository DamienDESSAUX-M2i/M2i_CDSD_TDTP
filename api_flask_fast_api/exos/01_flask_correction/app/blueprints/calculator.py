
from flask import Blueprint, jsonify, request

bp = Blueprint('calculator', __name__)



@bp.route('/calculate', methods=['GET'])
def calculate():
    try:
        operation = request.args.get('operation', '').lower()
        a_str = request.args.get('a')
        b_str = request.args.get('b')

        if not operation:
            return jsonify({
                'error': 'Missing parameter: operation',
                'valid_operations': ['add', 'subtract', 'multiply', 'divide']
            }), 400

        if not a_str or not b_str:
            return jsonify({'error': 'Missing parameters: a and b'}), 400

        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            return jsonify({
                'error': 'Parameters a and b must be valid numbers',
                'received': {'a': a_str, 'b': b_str}
            }), 400

        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                return jsonify({'error': 'Cannot divide by zero', 'a': a, 'b': b}), 400
            result = a / b
        else:
            return jsonify({
                'error': f'Unknown operation: {operation}',
                'valid_operations': ['add', 'subtract', 'multiply', 'divide']
            }), 400

        result = round(result, 10)
        return jsonify({'operation': operation, 'a': a, 'b': b, 'result': result}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
