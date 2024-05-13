import subprocess
import os
import time
import socket
import config
import threading
import sys
from utils import Colors as c

os.system('icacls startup.bat /grant Everyone:F')  # Granting permissions to everyone for startup.bat

pwd = os.getcwd()
print(f"================= {c.SELECTED}STARTING LACHAIN{c.ENDC} =================")

print("Starting bank server...")
subprocess.Popen(['start', 'cmd', '/k', 'startup.bat', 'server'], cwd=pwd, shell=True)
time.sleep(0.5)

for client in config.CLIENT_PORTS.keys():
    print(f'Starting {client}...')
    subprocess.Popen(['start', 'cmd', '/k', 'startup.bat', 'client', client], cwd=pwd, shell=True)
    time.sleep(0.5)

client_name = "CLI"

connections = {}

def receive(app):
    app.sendall(bytes(f'Client {client_name} connected', "utf-8"))
    while True:
        try:
            message = app.recv(config.BUFF_SIZE).decode()
            if not message:
                app.close()
                break
        except:
            app.close()
            break

def execute_command(seg_cmd):
    op_type = seg_cmd[0]

    if op_type == '#':
        return
    
    elif op_type == "wait":
        input(f"Press {c.BLINK}ENTER{c.ENDC} to continue simulation...")

    elif op_type == "balance":
        app = seg_cmd[1]
        if app == "server":
            connections[app].sendall(bytes("BALANCE", "utf-8"))
        elif app == "client":
            connections[seg_cmd[2]].sendall(bytes("BALANCE", "utf-8"))

    elif op_type == "transfer":
        from_c = seg_cmd[1]
        to_c = seg_cmd[2]
        amt = seg_cmd[3]
        connections[from_c].sendall(bytes(f'TRANSFER {to_c} {amt}', "utf-8"))

    elif op_type == "bchain":
        client = seg_cmd[1]
        connections[client].sendall(bytes("BLOCKCHAIN", "utf-8"))
    
    elif op_type == "delay":
        t = float(seg_cmd[1])
        time.sleep(t)
    
    else:
        print(f'{c.ERROR}Invalid command!{c.ENDC}')

def send():
    while True:
        command = input(">>> ").strip()
        if command != "":
            seg_cmd = command.split()
            op_type = seg_cmd[0]

            if op_type == "simulate":
                print('========== STARTING SIMULATION ==========')
                with open('simulate.txt') as f:
                    start_time = time.time()
                    for line in f.readlines():
                        if line.strip() != "":
                            if line.startswith('#'):
                                print(f'{c.VIOLET}{line}{c.ENDC}')
                            else:
                                print(f'{line}')
                            seg = line.strip().split()
                            execute_command(seg)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f'{c.BLUE}Execution time: {elapsed_time} seconds{c.ENDC}')
                print('========== SIMULATION COMPLETE ==========')
            
            elif op_type == "exit":
                for connection in connections.values():
                    # connection.sendall(bytes("EXIT", "utf-8"))
                    connection.close()
                sys.exit(0)

            else:
                execute_command(seg_cmd)

def connect_to(name, port):
    print(f'startup# Connecting to {name}...')
    connections[name] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections[name].setblocking(True)
    connections[name].connect((config.HOST, port))
    connections[name].sendall(bytes(client_name, "utf-8"))
    print(f"startup# {connections[name].recv(config.BUFF_SIZE).decode()}")
    thread = threading.Thread(target=receive, args=(connections[name],))
    thread.start()

if __name__ == "__main__":

    connect_to("server", config.BANK_PORT)

    for client, port in config.CLIENT_PORTS.items():
        connect_to(client, port)

    print(f"================= {c.SELECTED}SETUP COMPLETE{c.ENDC} =================")
    send()
