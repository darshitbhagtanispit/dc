from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket
import time

# client thread function used to receive bank operations
# Client thread function used to send bank operations to client side
def startReceivingOperations(slave_client):

    print("Enter your User ID:")
    user_id = input()
    slave_client.send(user_id.encode())

    while True:
        operations = """
        Bank Operations:
        1. Deposit
        2. Withdraw
        3. Check Balance
        4. Transaction History
        Enter operation number: """

        # Display operations on console
        print(operations)

        # Wait for user input for operation number
        operation_number = input()

        if operation_number in ['1', '2']:
            # Ask for amount if operation is deposit or withdraw
            amount = input("Enter amount: ")

        else:
            amount = None

        # Send operation number to master node
        slave_client.send(operation_number.encode())

        # Send amount to master node if applicable
        if amount:
            slave_client.send(amount.encode())

        time.sleep(5)


# function used to initiate the User Client / Slave Node
def initiateUserClient(port=8080):

    user_client = socket.socket()

    # connect to the bank server on local computer
    user_client.connect(('127.0.0.1', port))

    # start receiving bank operations
    print("Starting to receive bank operations from server\n")
    operation_thread = threading.Thread(target=startReceivingOperations, args=(user_client,))
    operation_thread.start()


# Driver function
if __name__ == '__main__':

    # initialize the User Client / Slave
    initiateUserClient(port=8080)
