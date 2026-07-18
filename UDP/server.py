import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


def receive():
    while True:
        try:
            data, addr = server.recvfrom(1024)
            messages.put((data, addr))
        except Exception:
            pass


def broadcast():
    while True:
        while not messages.empty():
            data, addr = messages.get()

            print(data.decode())

            if addr not in clients:
                clients.append(addr)

            for client in clients[:]:   # iterate over a copy
                try:
                    if data.decode().startswith("SIGNUP_TAGA:"):
                        name = data.decode().split(":", 1)[1]
                        server.sendto(f"{name} joined the chat".encode(), client)
                    else:
                        server.sendto(data, client)
                except Exception:
                    if client in clients:
                        clients.remove(client)


t1 = threading.Thread(target=receive, daemon=True)
t2 = threading.Thread(target=broadcast, daemon=True)

t1.start()
t2.start()

t1.join()
t2.join()