from flask import Flask, jsonify, request

def create_app() -> Flask:
    app = Flask(__name__)

    from .blueprints.hello import bp as hello_bp
    from .blueprints.converter import bp as converter_bp
    from .blueprints.books import bp as books_bp
    from .blueprints.registration import bp as registration_bp
    from .blueprints.calculator import bp as calculator_bp
    from .blueprints.posts import bp as posts_bp

    app.register_blueprint(hello_bp)
    app.register_blueprint(converter_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(calculator_bp)
    app.register_blueprint(posts_bp)

    register_error_handlers(app)
    return app



def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint not found',
            'path': request.path,
            'method': request.method
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method not allowed',
            'path': request.path,
            'method': request.method,
            'allowed_methods': 'GET, POST, PUT, DELETE'
        }), 405