import socket

class ChandyLamportSnapshotClient:
    def __init__(self, port=5552):
        self.server_address = ('127.0.0.1', port)

    def deposit(self, amount):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.server_address)
            client_socket.send(b'deposit')
            client_socket.send(str(amount).encode())
            response = client_socket.recv(1024).decode()
            print(response)

    def withdraw(self, amount):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.server_address)
            client_socket.send(b'withdraw')
            client_socket.send(str(amount).encode())
            response = client_socket.recv(1024).decode()
            print(response)

    def get_balance(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.server_address)
            client_socket.send(b'balance')
            balance = client_socket.recv(1024).decode()
            print("Current balance:", balance)

    def exit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.server_address)
            client_socket.send(b'exit')
            print("Exiting...")

if __name__ == "__main__":
    client = ChandyLamportSnapshotClient()
    client.get_balance()
    client.deposit(500)
    client.get_balance()
    client.withdraw(200)
    client.get_balance()
    client.exit()
