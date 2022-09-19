import sys
import socket
import threading
from threading import Thread
import queue

TerminateThreads = False
client_queue = queue.Queue()


def is_prime(n):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for divisor in range(3, n, 2):
        if n % divisor == 0:
            return False
    return True


def worker():
    _conn = None
    _addr = None
    work = False

    while True:
        try:
            if TerminateThreads:
                if work:
                    _conn.close()
                    print(f"{_addr} terminated")
                print(f"{Thread.name} terminated")
                break
            if not work:
                if client_queue.empty():
                    continue
                else:
                    _conn, _addr = client_queue.get(block=False)
                    work = True
                    print(f"{_addr} connected")
            number = _conn.recv(1024).decode()

            if not number:
                print(f"{_addr} disconnected")
                _conn.close()
                _conn = None
                _addr = None
                work = False
            else:
                if is_prime(int(number)):
                    _conn.send(f"{number} is prime".encode())
                else:
                    _conn.send(f"{number} is not prime".encode())
        except:
            continue


port = int(sys.argv[1])
sock = socket.socket()
sock.bind(("localhost", port))
sock.listen()

threads = [threading.Thread(target=worker)
           for i in range(0, 3)]

for thread in threads:
    thread.start()

while True:
    try:
        client, addr = sock.accept()
        client_queue.put((client, addr), block=True)
    except KeyboardInterrupt:
        print("\rShutting down")
        TerminateThreads = True
        for thread in threads:
            thread.join()
        print("Done")
        break

