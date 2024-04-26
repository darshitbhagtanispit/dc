import socket
import threading
import random
import time

class VectorClockThreads:
    def __init__(self, operation):
        self.operation = operation

    def initialize_map(self):
        self.server_map = {
            "glados": 0,
            "yes": 1,
            "rhea": 2
        }

    def run(self):
        if self.operation == "sender":
            time.sleep(5)
            print(self.operation)
            self.select_an_event()
            print("-------------------------")
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("localhost", 5553))
            server_socket.listen(1)

            while True:
                client_socket, address = server_socket.accept()
                print("Connection established")
                data = client_socket.recv(1024).decode()
                sending_server, current_server, amount, vector_incoming = data.split("#")
                self.process_the_incoming_array_string(vector_incoming, current_server)
                self.balance += int(amount)
                print("Vector clock at {} Process is:".format(current_server))
                print(self.vector_time)
                client_socket.close()

    def process_the_incoming_array_string(self, vector_incoming, current_server):
        vector_time = [int(x) for x in vector_incoming.split(",")]
        index = self.server_map[current_server]
        self.vector_time[index] += 1
        self.vector_time = [max(x, y) for x, y in zip(self.vector_time, vector_time)]

    def select_an_event(self):
        option = random.randint(0, 2)
        if option == 0:
            print("Deposit Selected")
            self.deposit()
        elif option == 1:
            print("Withdraw Selected")
            self.withdraw()
        else:
            print("Transfer Selected")
            self.transfer()

    def deposit(self):
        amount = random.randint(1, 100)
        print("Amount to deposit is:", amount)
        self.balance += amount
        print("Balance after deposit is:", self.balance)
        self.vector_time[self.server_index] += 1
        print("Vector clock at {} Process is:".format(self.server_name))
        print(self.vector_time)

    def withdraw(self):
        amount = random.randint(1, 100)
        print("Amount to withdraw is:", amount)
        if self.balance - amount >= 0:
            self.balance -= amount
            print("Balance after withdraw is:", self.balance)
            self.vector_time[self.server_index] += 1
            print("Vector clock at {} Process is:".format(self.server_name))
            print(self.vector_time)
        else:
            print("Insufficient Funds, Event can't occur")

    def transfer(self):
        amount = random.randint(1, 100)
        print("Amount to transfer is:", amount)
        if self.balance - amount >= 0:
            self.balance -= amount
            transfer_to = random.choice([x for x in range(3) if x != self.server_index])
            self.vector_time[self.server_index] += 1
            print("Transferring... to", server_list[transfer_to])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 5553))
                s.sendall("{}#{}#{}#{}".format(self.server_name, server_list[transfer_to], amount, self.vector_time).encode())
                print("Transferred to:", server_list[transfer_to])
        else:
            print("Insufficient Funds, Event can't occur")

# Inside the main block

if __name__ == "__main__":
    server_list = ["glados", "yes", "rhea","LAPTOP-TAHP3R9R"]
    server_name = socket.gethostname()
    server_index = server_list.index(server_name)
    vector_time = [0, 0, 0]
    balance = 1000
    
    obj = VectorClockThreads("receiver")
    obj.initialize_map()
    receiver_thread = threading.Thread(target=obj.run)
    receiver_thread.start()

    time.sleep(3)

    obj = VectorClockThreads("sender")
    obj.server_name = server_name
    obj.server_index = server_index
    obj.vector_time = vector_time
    obj.balance = balance
    sender_thread = threading.Thread(target=obj.run)
    sender_thread.start()

    receiver_thread.join()
    sender_thread.join()

