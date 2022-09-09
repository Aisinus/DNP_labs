import sys
from socket import *
import time


class Client:
    def __init__(self, seqn, filename, size):
        self.seqn = seqn
        self.filename = filename
        self.size = size
        self.data = None
        self.time = None
        self.full_file = False
        self.start_message = False

    def start_time(self):
        self.time = time.time()

    def get_time(self):
        return time.time() - self.time

    def set_seqn(self, seqn):
        self.seqn = seqn

    def add_data(self, new_data):
        if self.data is None:
            self.data = new_data
        else:
            self.data += new_data
        self.start_message = True


port = int(sys.argv[1])
localhost = "localhost"
s = socket(AF_INET, SOCK_DGRAM)
s.setblocking(False)
s.bind((localhost, port))

buff = 1024
clients = {}

while True:
    try:
        msg_data, address_client = s.recvfrom(buff)
        msg_type = msg_data.split(" | ".encode())[0]
        msg_type = msg_type.decode()
        if msg_type == "s":
            seqn, filename, file_size = msg_data.decode().split(" | ")[1:4]

            if not (address_client in clients):
                clients[address_client] = Client(int(seqn), filename, int(file_size))
                ack_msg = f"a | {int(seqn) + 1} | {buff}".encode()
                print(f"start session with {address_client[0]}:{address_client[1]}")
            else:
                ack_msg = f"a | {clients[address_client].seqn + 1}".encode()

            s.sendto(ack_msg, address_client)
            clients[address_client].start_time()

        elif msg_type == "d" and (address_client in clients):
            seqn = msg_data.split(" | ".encode())[1]
            data_bytes = " | ".encode().join(msg_data.split(" | ".encode())[2:])
            if int(seqn) == clients[address_client].seqn + 1:
                clients[address_client].add_data(data_bytes)
                clients[address_client].set_seqn(int(seqn))
                ack_msg = f"a | {int(seqn) + 1}".encode()
                s.sendto(ack_msg, address_client)
                clients[address_client].start_time()
            else:
                ack_msg = f"a | {clients[address_client].seqn + 1}".encode()
                s.sendto(ack_msg, address_client)
                clients[address_client].start_time()



    except:
        for addr, client in list(clients.items()):
            if client.start_message:
                if client.size == len(client.data) and client.full_file is False:
                    print(f"Get file from {addr[0]}:{addr[1]}")
                    client.full_file = True
                    new_file = open(client.filename, "wb")
                    new_file.write(client.data)
                    new_file.close()
                    client.start_time()
                elif client.size == len(client.data) and client.full_file is True and client.get_time() >= 1:
                    print(f"{addr[0]}:{addr[1]} was deleted from list")
                    del clients[addr]

                if client.get_time() >= 3:
                    print(f"client {addr[0]}:{addr[1]} inactive too long")
                    del clients[addr]