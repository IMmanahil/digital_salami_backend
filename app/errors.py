import logging
from flask import jsonify

logger = logging.getLogger("DigitalSalami")

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, 'description', str(error))
        response = jsonify({"error": "Bad request", "message": message})
        response.status_code = 400
        logger.warning(f"400 Bad Request: {message}")
        return response

    @app.errorhandler(401)
    def unauthorized(error):
        message = getattr(error, 'description', str(error))
        response = jsonify({"error": "Unauthorized", "message": message})
        response.status_code = 401
        logger.warning(f"401 Unauthorized: {message}")
        return response

    @app.errorhandler(404)
    def not_found(error):
        response = jsonify({"error": "Resource not found"})
        response.status_code = 404
        logger.warning(f"404 Not Found: {error}")
        return response

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}", exc_info=True)
        response = jsonify({"error": "Internal server error"})
        response.status_code = 500
        return response
