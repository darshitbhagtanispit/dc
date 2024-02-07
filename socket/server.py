import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)

class BankServer:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, account_number, initial_balance):
        self.accounts[account_number] = initial_balance
        return f"Account {account_number} created with initial balance: {initial_balance}"

    def get_balance(self, account_number):
        return self.accounts.get(account_number, "Account not found")

    def deposit(self, account_number, amount):
        if account_number in self.accounts:
            self.accounts[account_number] += amount
            return f"Deposited {amount} into account {account_number}. New balance: {self.accounts[account_number]}"
        else:
            return "Account not found"

    def withdraw(self, account_number, amount):
        if account_number in self.accounts and self.accounts[account_number] >= amount:
            self.accounts[account_number] -= amount
            return f"Withdrew {amount} from account {account_number}. New balance: {self.accounts[account_number]}"
        else:
            return "Insufficient funds or account not found"

    def exit(self):
        # Any cleanup or finalization code can be added here
        return "Exiting the banking system. Goodbye!"


    # Existing methods remain unchanged

server = BankServer()

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")  # Display client connection message

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")  # Display client disconnection message

@sio.event
def execute_option(sid, data):
    option = data['option']
    account_number = data['account_number']
    amount = data['amount']
    if option == 1:
        result = server.create_account(account_number, amount)
    elif option == 2:
        result = server.get_balance(account_number)
    elif option == 3:
        result = server.deposit(account_number, amount)
    elif option == 4:
        result = server.withdraw(account_number, amount)
    else:
        result = "Invalid option"
    print(result)  # Display the result in the server's terminal
    sio.emit('result', {'result': result}, room=sid)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)