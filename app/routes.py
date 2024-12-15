from flask import Flask, request, jsonify
from .models import User, Transaction, db
from .extensions import ma

app = Flask(__name__)


@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    """
           Create a new transaction
           ---
           parameters:
             - name: amount
               in: body
               type: float
               required: true
           responses:
               201:
                 description: Transaction created
           """
    data = request.get_json()
    amount = data.get('amount')
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    transaction = Transaction(amount=amount, user_id=user_id)
    transaction.calculate_commission()
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"id": transaction.id, "amount": transaction.amount, "commission": transaction.commission}), 201


@app.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    if transaction.status == 'pending':
        transaction.status = 'canceled'
        db.session.commit()
        return jsonify({"status": "Transaction canceled"})
    return jsonify({"error": "Transaction cannot be canceled"}), 400


@app.route('/check_transaction', methods=['GET'])
def check_transaction():
    transaction_id = request.args.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({"transaction_id": transaction.id, "status": transaction.status})


