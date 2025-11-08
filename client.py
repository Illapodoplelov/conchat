from socket import *
import threading

client_socket = socket(AF_INET,SOCK_STREAM)
name = input("Введіть ім'я: ")
client_socket.connect(('localhost', 12345))
client_socket.send(name.encode())

status = "active"

def send_message():
    while True:
        if status == "muted":
            print("⛔ Ви замучені. Повідомлення не можуть бути надіслані.")
            continue
        client_message = input("💬 Введіть повідомлення ('exit' для виходу): ").strip()
        if client_message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(client_message.encode())

threading.Thread(target=send_message).start()

while True:
    try:
        message = client_socket.recv(1024).decode().strip()
        if message:
            print(message)

            if f"{name} був замучен" in message or "Ви в муті" in message:
                status = "muted"
    except:
        print("🔌 З'єднання з сервером втрачено.")
        break

































