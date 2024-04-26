# server/app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS 


from transaction_records import TransactionRecorder

app = Flask(__name__)
transaction_recorder = TransactionRecorder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_transaction', methods=['POST'])
def process_transaction():
    username = request.form['username']
    operation = request.form['operation']
    amount = float(request.form['amount']) if 'amount' in request.form else None

    user_id = transaction_recorder.get_user_id(username)
    if user_id is None:
        return jsonify({'success': False, 'message': 'User not found'})

    if operation == 'deposit':
        if amount is None:
            return jsonify({'success': False, 'message': 'Amount required for deposit'})
        transaction_recorder.deposit(user_id, amount)
        return jsonify({'success': True, 'message': f'Deposited {amount} successfully'})

    elif operation == 'withdraw':
        if amount is None:
            return jsonify({'success': False, 'message': 'Amount required for withdrawal'})
        if not transaction_recorder.withdraw(user_id, amount):
            return jsonify({'success': False, 'message': 'Insufficient funds'})
        return jsonify({'success': True, 'message': f'Withdrawn {amount} successfully'})

    elif operation == 'check_balance':
        balance = transaction_recorder.get_balance(user_id)
        return jsonify({'success': True, 'message': f'Your balance is {balance}'})

    elif operation == 'view_transactions':
        transactions = transaction_recorder.get_transactions(user_id)
        return jsonify({'success': True, 'transactions': transactions})

if __name__ == '__main__':
    app.run(debug=True)
