import sys
import socket

address, port = sys.argv[1].split(":")
server_address = (address, int(port))

numbers = [15492781, 15492787, 15492803,
           15492811, 15492810, 15492833,
           15492859, 15502547, 15520301,
           15527509, 15522343, 1550784]

conn = socket.socket()
conn.connect(server_address)
print(f"Connected to {server_address}")

try:
    for number in numbers:
        conn.send(str(number).encode())
        answer = conn.recv(1024).decode()
        print(f"{answer}")
    print("Complete")
except ConnectionError:
    print("Server terminate connection")
    sys.exit()
