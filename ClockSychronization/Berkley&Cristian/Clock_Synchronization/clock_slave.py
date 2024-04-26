import socket
import time
import datetime

def synchronize_time(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        
        while True:
            print("\n1. Deposit")
            print("2. Withdrawal")
            print("3. Check Balance")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                amount = float(input("Enter the amount to deposit: "))
                message = f"Deposit:{amount}"
            elif choice == '2':
                amount = float(input("Enter the amount to withdraw: "))
                message = f"Withdraw:{amount}"
            elif choice == '3':
                message = "CheckBalance"
            elif choice == '4':
                message = "Exit"
                client_socket.send(message.encode())
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            # Send request to server
            client_socket.send(message.encode())
            
            if choice != '4':
                # Receive response from server
                response = client_socket.recv(1024).decode()
                print(response)

if __name__ == "__main__":
    synchronize_time(('127.0.0.1', 8080))
