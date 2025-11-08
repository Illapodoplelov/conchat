from socket import * 
import threading
import time 
seconds = 30
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(10)
print('Server running...')

clients = []
clients_names = {}
muted_users = set()
spam_tracker = {}
def broadcast(message):
    for client in clients:
        try:
            client.send(f"{message}\n".encode())
        except:
            print("Помилка відправки")

def anti_spam(name, message):
    now = time.time()
    if name not in spam_tracker:
        spam_tracker[name] = []
    spam_tracker[name].append((message, now))

    # Удаляем старые сообщения
    spam_tracker[name] = [
        (msg, t) for msg, t in spam_tracker[name] if now - t <= 10
    ]

    # Проверка на одинаковые сообщения
    messages = [msg for msg, _ in spam_tracker[name]]
    if messages.count(message) >= 5:
        mute(name)
        broadcast(f"{name} був замучен за спам.", sender=name)

# Функция мута пользователя
def mute(name):
    muted_users.add(name)
    print(f"Користувач {name} замучен.")


def handle_client(client_socket):
    name = client_socket.recv(1024).decode().strip()
    broadcast(f"{name} joined!")
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            broadcast(f"{name}: {message}")
        except:
            clients.remove(client_socket)
            broadcast(f"{name} left!")
            client_socket.close()
            break
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()









































