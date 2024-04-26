import socket
import threading
import datetime

def handle_client(conn, addr):
    while True:
        try:
            # Receive request from client
            request = conn.recv(1024).decode()
            if not request:
                break
            
            if request == "Exit":
                print(f"Client at address {addr} exited.")
                break
            
            # Process client request
            response = process_request(request)
            
            # Respond to client
            conn.send(response.encode())
            
        except ConnectionResetError:
            print(f"Connection with {addr} closed unexpectedly.")
            break
        
    # Close connection
    conn.close()

def process_request(request):
    if request.startswith("Deposit"):
        amount = float(request.split(":")[1])
        # Perform deposit operation (dummy implementation)
        return f"Deposit successful. Amount: {amount}"
    
    elif request.startswith("Withdraw"):
        amount = float(request.split(":")[1])
        # Perform withdrawal operation (dummy implementation)
        return f"Withdrawal successful. Amount: {amount}"
    
    elif request == "CheckBalance":
        # Perform check balance operation (dummy implementation)
        balance = 1000  # Dummy balance for demonstration
        return f"Your balance: {balance}"
    
    else:
        return "Invalid request."

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    
    print("Server started...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        
        # Handle client request in a new thread
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server(8080)
