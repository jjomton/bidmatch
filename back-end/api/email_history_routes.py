from flask import Blueprint, jsonify, request

from services.email_service import EmailService

email_history_bp = Blueprint("email_histories", __name__)
email_service = EmailService()


@email_history_bp.get("")
def list_email_histories():
    user_id = request.args.get("userId")
    return jsonify({"items": email_service.list_histories(user_id)})
