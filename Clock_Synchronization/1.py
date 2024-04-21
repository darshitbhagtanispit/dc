from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket
import time

# Bank account data
bank_account = {
    'balance': 1000,
    'transactions': []
}
client_data = {} 
# Client thread function used to send bank operations to client side
# client thread function used to receive bank operations
def startSendingOperations(slave_client):

    # Receive user ID from slave node
    user_id = slave_client.recv(1024).decode().strip()
    print(f"User {user_id} has entered.")

    while True:
        print("Waiting to receive operation number...")
        
        # Receive operation number from slave node
        operation_number = slave_client.recv(1024).decode().strip()
        print(f"Received operation number: {operation_number}")

        # Receive amount from slave node if applicable
        if operation_number in ['1', '2']:
            amount = float(slave_client.recv(1024).decode().strip())
            print(f"Received amount: {amount}")
        else:
            amount = None

        response = ""

        if operation_number == '1':
            deposit(amount)
            response = f"User {user_id} deposited {amount}. New Balance: {bank_account['balance']}"

        elif operation_number == '2':
            withdraw(amount)
            response = f"User {user_id} withdrew {amount}. New Balance: {bank_account['balance']}"

        elif operation_number == '3':
            check_balance()
            response = f"User {user_id} checked balance. Balance: {bank_account['balance']}"

        elif operation_number == '4':
            transaction_history(user_id)
            response = f"User {user_id} viewed transaction history."

        # Send response to slave node
        slave_client.send(response.encode())

        time.sleep(5)

def deposit(amount,user_id):
    bank_account['balance'] += amount
    bank_account['transactions'].setdefault(user_id, []).append(f"Deposited {amount} on {datetime.datetime.now()}")

def withdraw(amount,user_id):
    if amount <= bank_account['balance']:
        bank_account['balance'] -= amount
        bank_account['transactions'].setdefault(user_id, []).append(f"Withdrew {amount} on {datetime.datetime.now()}")
    else:
        print("Insufficient balance")

def check_balance():
    print(f"Current Balance: {bank_account['balance']}")

def transaction_history(user_id):
    print("Transaction History:")
    for transaction in bank_account['transactions'].get(user_id, []):
        print(transaction)

def startRecieveingClockTime(connector, address): 

	while True: 
		# recieve clock time 
		clock_time_string = connector.recv(1024).decode() 
		clock_time = parser.parse(clock_time_string) 
		clock_time_diff = datetime.datetime.now() - clock_time 

		client_data[address] = { 
					"clock_time"	 : clock_time, 
					"time_difference" : clock_time_diff, 
					"connector"	 : connector 
					} 

		print("Client Data updated with: "+ str(address), end = "\n\n") 
		time.sleep(5) 
def startConnecting(master_server): 
	
	# fetch clock time at slaves / clients 
	while True: 
		# accepting a client / slave clock client 
		master_slave_connector, addr = master_server.accept() 
		slave_address = str(addr[0]) + ":" + str(addr[1]) 

		print(slave_address + " got connected successfully") 

		current_thread = threading.Thread( 
						target = startRecieveingClockTime, 
						args = (master_slave_connector, slave_address, )) 
		current_thread.start() 
# Bank operations
def deposit(amount):
    bank_account['balance'] += amount
    bank_account['transactions'].append(f"Deposited {amount} on {datetime.datetime.now()}")

def withdraw(amount):
    if amount <= bank_account['balance']:
        bank_account['balance'] -= amount
        bank_account['transactions'].append(f"Withdrew {amount} on {datetime.datetime.now()}")
    else:
        print("Insufficient balance")

def check_balance():
    print(f"Current Balance: {bank_account['balance']}")

def transaction_history():
    print("Transaction History:")
    for transaction in bank_account['transactions']:
        print(transaction)


# function used to initiate the Bank Server / Master Node
def initiateBankServer(port=8080):

    bank_server = socket.socket()
    bank_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket at bank created successfully\n")

    bank_server.bind(('', port))

    # Start listening to requests
    bank_server.listen(10)
    print("Bank server started...\n")

    # start making connections
    print("Starting to make connections...\n")
    bank_thread = threading.Thread(target=startConnecting, args=(bank_server,))
    bank_thread.start()

    # start sending bank operations
    print("Starting to send bank operations to clients...\n")
    operation_thread = threading.Thread(target=startSendingOperations, args=(bank_server,))
    operation_thread.start()


# Driver function
if __name__ == '__main__':

    # Trigger the Bank Server
    initiateBankServer(port=8080)
