# server/transaction_records.py
import mysql.connector

class TransactionRecorder:
    def __init__(self, host="localhost", user="root", password="", database="banks"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), balance DECIMAL(10, 2))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                          (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, transaction_text TEXT,
                           FOREIGN KEY (user_id) REFERENCES users(id))''')
        self.conn.commit()


    def add_user(self, username, balance=0):
        self.cursor.execute("INSERT INTO users (username, balance) VALUES (%s, %s)", (username, balance))
        self.conn.commit()

    def get_user_id(self, username):
        self.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def deposit(self, user_id, amount):
        self.cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        self.conn.commit()
        self.add_transaction(user_id, f"Deposited {amount}")

    def withdraw(self, user_id, amount):
        balance = self.get_balance(user_id)
        if balance is not None and balance >= amount:
            self.cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
            self.conn.commit()
            self.add_transaction(user_id, f"Withdrew {amount}")
            return True
        else:
            return False

    def get_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def add_transaction(self, user_id, transaction):
        self.cursor.execute("INSERT INTO transactions (user_id, transaction_text) VALUES (%s, %s)", (user_id, transaction))
        self.conn.commit()

    def get_transactions(self, user_id):
        self.cursor.execute("SELECT transaction_text FROM transactions WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

