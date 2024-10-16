import socket
import threading
from tkinter import *

# Función para enviar mensaje al servidor
def send_message(client_socket, entry, log_area):
    message = entry.get()
    client_socket.send(message.encode('utf-8'))
    log_area.insert(END, f"Tú: {message}\n")
    entry.delete(0, END)

# Función para recibir mensajes del servidor
def receive_messages(client_socket, log_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            log_area.insert(END, f"Servidor: {message}\n")
        except ConnectionResetError:
            break

# Interfaz Gráfica para el Cliente
def create_client_interface():
    root = Tk()
    root.title("Cliente TCP")

    frame = Frame(root)
    frame.pack()

    # Sección para el nombre de usuario
    label_username = Label(frame, text="Nombre de usuario:")
    label_username.pack()
    username_entry = Entry(frame, width=50)
    username_entry.pack()

    # Sección para los mensajes después de la conexión
    label_message = Label(frame, text="Escribe tu mensaje:")
    label_message.pack_forget()  # Se oculta al inicio
    message_entry = Entry(frame, width=50)
    message_entry.pack_forget()  # Se oculta al inicio

    log_area = Text(frame, height=10, width=50)
    log_area.pack()

    # Botón para enviar el mensaje
    send_button = Button(frame, text="Enviar", command=lambda: send_message(client_socket, message_entry, log_area))
    send_button.pack_forget()  # Se oculta al inicio

    # Función para conectar al servidor
    def connect_to_server():
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.43.96', 9999)) #Se debe modificar la IP

        # Enviar nombre de usuario al servidor
        username = username_entry.get()
        client_socket.send(username.encode('utf-8'))

        log_area.insert(END, f"Conectado como {username}\n")
        threading.Thread(target=receive_messages, args=(client_socket, log_area)).start()

        # Hacer visible la parte de mensajes después de conectar
        label_message.pack()
        message_entry.pack()
        send_button.pack()
        label_username.pack_forget()
        username_entry.pack_forget()
        connect_button.pack_forget()

    # Botón para conectar
    connect_button = Button(frame, text="Conectar", command=connect_to_server)
    connect_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_client_interface()