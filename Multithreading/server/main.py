# server/main.py
from banking_logic import BankAccount
from transaction_records import TransactionRecorder

def main():
    # MySQL database connection details
    host = "localhost"
    user = "root"
    password = ""
    database = "banks"

    account = BankAccount(1000)
    transaction_recorder = TransactionRecorder(host, user, password, database)

    # Main logic here

    transaction_recorder.close_connection()

if __name__ == "__main__":
    main()
