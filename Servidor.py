import socket
import threading
from tkinter import *

clients = {}  # Diccionario para almacenar los sockets de los clientes y sus nombres de usuario

# Función para manejar la conexión de cada cliente
def handle_client(client_socket, client_address, log_area, clients_listbox):
    try:
        # Recibir el nombre de usuario del cliente
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        log_area.insert(END, f"[+] {username} ({client_address}) se ha conectado.\n")
        clients_listbox.insert(END, username)  # Agregar el cliente a la lista visual

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                log_area.insert(END, f"[{username}] {message}\n")
            else:
                break
    except ConnectionResetError:
        pass
    finally:
        log_area.insert(END, f"[-] {username} ({client_address}) se ha desconectado.\n")
        client_socket.close()
        clients_listbox.delete(clients_listbox.get(0, END).index(username))  # Eliminar de la lista visual
        del clients[client_socket]  # Remover el cliente de la lista

# Función para enviar mensaje a todos los clientes
def broadcast(message, log_area):
    log_area.insert(END, f"Enviando a todos: {message}\n")
    for client_socket in clients:
        client_socket.send(message.encode('utf-8'))

# Función para enviar mensaje a un cliente específico
def send_to_client(selected_username, message, log_area):
    for client_socket, client_username in clients.items():
        if client_username == selected_username:
            client_socket.send(message.encode('utf-8'))
            log_area.insert(END, f"Enviando a {selected_username}: {message}\n")
            break

# Función para iniciar el servidor
def start_server(log_area, clients_listbox):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    log_area.insert(END, "[*] Servidor escuchando en el puerto 9999\n")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, log_area, clients_listbox))
        client_handler.start()

# Interfaz Gráfica con Tkinter
def create_server_interface():
    root = Tk()
    root.title("Servidor Multihilo")

    frame = Frame(root)
    frame.pack()

    # Área de log para mostrar los mensajes
    log_area = Text(frame, height=20, width=50)
    log_area.pack(side=LEFT)

    # Lista de clientes conectados
    clients_listbox = Listbox(frame, height=20, width=20)
    clients_listbox.pack(side=LEFT)

    # Área para escribir mensajes
    message_entry = Entry(frame, width=50)
    message_entry.pack()

    # Botón para enviar mensaje a todos
    broadcast_button = Button(frame, text="Enviar a todos", command=lambda: broadcast(message_entry.get(), log_area))
    broadcast_button.pack()

    # Botón para enviar mensaje a cliente seleccionado
    send_to_client_button = Button(frame, text="Enviar a cliente", command=lambda: send_to_client(clients_listbox.get(ACTIVE), message_entry.get(), log_area))
    send_to_client_button.pack()

    # Botón para iniciar el servidor
    start_button = Button(frame, text="Iniciar Servidor", command=lambda: threading.Thread(target=start_server, args=(log_area, clients_listbox)).start())
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_server_interface()