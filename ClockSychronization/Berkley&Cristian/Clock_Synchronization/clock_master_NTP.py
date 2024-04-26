import socket
import threading
import time

class ChandyLamportSnapshotServer:
    def __init__(self, port=5552):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.balance = 1000
        self.attached_channels = {"glados": 0, "yes": 0, "rhea": 0}
        self.marker = 0
        self.marker_list = set()
        self.state_recorded = False
        self.temp = 0
        self.acknowledgement = {"glados": False, "yes": False, "rhea": False}

    def handle_client(self, conn, addr):
        while True:
            try:
                request = conn.recv(1024).decode()
                if not request:
                    break
                if request == "exit":
                    print(f"Client at address {addr} exited.")
                    break
                elif request == "balance":
                    conn.send(str(self.balance).encode())
                elif request == "deposit":
                    amount = int(conn.recv(1024).decode())
                    self.balance += amount
                    conn.send("Deposit successful".encode())
                elif request == "withdraw":
                    amount = int(conn.recv(1024).decode())
                    if amount <= self.balance:
                        self.balance -= amount
                        conn.send("Withdrawal successful".encode())
                    else:
                        conn.send("Insufficient funds".encode())
            except Exception as e:
                print("Error:", e)
                break
        conn.close()

    def start_server(self):
        self.server_socket.bind(('127.0.0.1', self.port))
        self.server_socket.listen(5)
        print("Server started...")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr} established!")
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    server = ChandyLamportSnapshotServer()
    server.start_server()
