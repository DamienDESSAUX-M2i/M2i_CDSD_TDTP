from flask import Flask, request, jsonify, Blueprint

# Exercice 1: Hello World Multilingue

TRANSLATIONS = {
    'english': 'Hello!',
    'french': 'Bonjour!',
    'spanish': '¡Hola!',
    'german': 'Hallo!',
    'italian': 'Ciao!',
    'portuguese': 'Olá!'
}

#app = Flask(__name__)

bp = Blueprint('hello',__name__)


@bp.route('/hello/<language>', methods=['GET'])
def hello(language):
    """
    Route 1: Hello World multilingue

    Utilise:
    - Route parameter: <language>
    - Gestion d'erreur: 404 si langue non trouvée
    - Retour JSON avec jsonify()

    Exemple:
        GET /hello/french
        → {"message": "Bonjour!", "language": "french"}
    """

    if language not in TRANSLATIONS:
        return jsonify({
            'error': 'Language not found',
            'available': list(TRANSLATIONS.keys())
        }), 404

    return jsonify({
        'message': TRANSLATIONS[language],
        'language': language
    }), 200


# app.run(debug=True,port=5000,host='0.0.0.0')