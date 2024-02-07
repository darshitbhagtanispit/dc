import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def result(data):
    print(data['result'])

def main():
    sio.connect('http://localhost:5000')

    while True:
        print("Options:")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Exit")

        choice = int(input("Enter your choice (1-5): "))

        if choice == 5:
            sio.disconnect()
            break

        account_number = input("Enter account number: ")

        if choice in [1, 3, 4]:  # Create, Deposit, or Withdraw
            amount = float(input("Enter amount: "))
            sio.emit('execute_option', {'option': choice, 'account_number': account_number, 'amount': amount})
        elif choice == 2:  # Check Balance
            sio.emit('execute_option', {'option': choice, 'account_number': account_number, 'amount': None})
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

if __name__ == "__main__":
    main()