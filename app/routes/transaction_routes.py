from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from app import db
import logging

logger = logging.getLogger("DigitalSalami")

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/test', methods=['GET'])
def test_transaction():
    logger.info("/transaction/test hit")
    return jsonify({"message": "Transaction route is working"}), 200


@transaction_bp.route('/send', methods=['POST'])
@jwt_required()
def send_transaction():
    logger.info("📨 Received salami transaction request")

    data = request.get_json()
    if not data:
        logger.warning("Request body missing")
        abort(400, description="Request body is missing")

    required_fields = ['sender_name', 'sender_email', 'receiver_name', 'receiver_email', 'amount', 'payment_method']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        logger.warning(f"❗ Missing fields in transaction: {missing_fields}")
        abort(400, description=f"Missing fields: {', '.join(missing_fields)}")

    # Attempt to create transaction (if this fails, it will raise an exception)
    txn = Transaction(
        sender_name=data['sender_name'],
        sender_email=data['sender_email'],
        receiver_name=data['receiver_name'],
        receiver_email=data['receiver_email'],
        amount=float(data['amount']),
        payment_method=data['payment_method'],
        status='success',  # For now, default to success; can be updated via webhook
        user_id=get_jwt_identity()
    )

    db.session.add(txn)
    db.session.commit()

    logger.info(f"Transaction saved successfully. ID: {txn.id}")
    return jsonify({
        "message": "Transaction saved successfully",
        "transaction_id": txn.id
    }), 201
