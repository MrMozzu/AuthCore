from flask import jsonify 
from marshmallow import ValidationError
from app.errors.exceptions import APIException

def handle_validation_errors(error):

    return jsonify({
        "success": False,
        "message": "Validation Error",
        "errors": error.messages,
    }), 400

def handle_api_exception(error):

    return jsonify({
        "success": False,
        "message": error.message,
    }), error.status


def handle_generic_exception(error):

    return jsonify({
        "success": False,
        "message": "Internal Server Error"
    }), 500


def register_error_handlers(app):

    app.register_error_handler(
        ValidationError,
        handle_validation_errors
    )

    app.register_error_handler(
        APIException,
        handle_api_exception
    )

    app.register_error_handler(
        Exception,
        handle_generic_exception
    )
