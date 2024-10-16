# Sockets-Multihilo
Actividad Servidor y Cliente con Sockets Multihilo en Python.


# **Servidor y Cliente TCP Multihilo con GUI utilizando Tkinter**

## **Descripción del Proyecto**

Este proyecto implementa un sistema cliente-servidor utilizando **sockets** en Python, con una interfaz gráfica de usuario (GUI) desarrollada en **Tkinter**. La aplicación permite establecer comunicación TCP entre múltiples clientes y un servidor, facilitando la interacción en tiempo real. El servidor puede gestionar varios clientes simultáneamente usando **multihilos**. Los clientes pueden enviar y recibir mensajes, tanto de manera individual como a todos los usuarios conectados.

## **Estructura del Proyecto**

-   **Servidor Multihilo:** Permite gestionar múltiples conexiones de clientes, enviar mensajes a todos los clientes o a un cliente específico.
-   **Cliente TCP:** Permite conectarse al servidor y enviar mensajes en tiempo real.
-   **Interfaz Gráfica:** Implementada con **Tkinter** para facilitar la interacción del usuario.

## **Requisitos**

1.  **Python 3.x** instalado.
2.  Biblioteca **Tkinter** (incluida por defecto con Python).
3.  Acceso a una red local para la comunicación cliente-servidor.
4.  Editor de código y Git para gestionar el repositorio.

## **Ejecución del Proyecto**

### **1. Servidor**

1.  Abre una terminal y navega al directorio donde está el código del servidor.
    
2.  Ejecuta el siguiente comando:
    ```
    python Servidor.py
    ```
3.  En la interfaz gráfica del servidor:
    
    -   Haz clic en "Iniciar Servidor" para comenzar a escuchar en el puerto 9999.
    -   A medida que los clientes se conectan, sus nombres aparecerán en la lista.
    -   Puedes enviar mensajes a todos los clientes o a un cliente específico.
   
   ### **2. Cliente**

1.  Abre otra terminal y navega al directorio donde está el código del cliente.
2.  Edita el archivo Cliente.py y busca la línea 52 para editar la IP a la del dispositivo que funciona como servidor. Puedes averiguar la IP ejecutando en CMD el siguiente comando en la máquina servidor:
    ```
	ipconfig
	```
    
3.  Ejecuta el siguiente comando:
	```
	python Cliente.py
	```
    
3.  Ingresa el **nombre de usuario** y presiona "Conectar".
    
4.  Una vez conectado, puedes:
    
    -   Escribir y enviar mensajes al servidor desde la interfaz.
    -   Recibir mensajes enviados por el servidor.
 
 ## **Arquitectura del Proyecto**

### **Servidor**

-   **Socket TCP/IP:** Configurado para escuchar en `0.0.0.0` en el puerto 9999.
-   **Multihilos:** Cada conexión de cliente se maneja en un hilo separado.
-   **Broadcast:** Permite enviar un mensaje a todos los clientes conectados.
-   **Comunicación Individual:** Se puede seleccionar un cliente específico para enviarle un mensaje.

### **Cliente**

-   **Conexión al Servidor:** El cliente se conecta al servidor por su dirección IP y puerto.
-   **Comunicación:** Permite enviar mensajes y recibir mensajes en tiempo real.
-   **Interfaz en Tkinter:** Facilita la interacción del usuario con el sistema.

## **Código del Proyecto**

### **Servidor**
```python
import  socket
import  threading
from  tkinter  import  *

clients  = {} # Diccionario para almacenar los sockets de los clientes y sus nombres de usuario

# Función para manejar la conexión de cada cliente
def  handle_client(client_socket, client_address, log_area, clients_listbox):
	try:
		# Recibir el nombre de usuario del cliente
		username  =  client_socket.recv(1024).decode('utf-8')
		clients[client_socket] =  username
		log_area.insert(END, f"[+] {username} ({client_address}) se ha conectado.\n")
		clients_listbox.insert(END, username) # Agregar el cliente a la lista visual
		
		while  True:
			message  =  client_socket.recv(1024).decode('utf-8')
			if  message:
				log_area.insert(END, f"[{username}] {message}\n")
			else:
				break
	except  ConnectionResetError:
		pass
	finally:
		log_area.insert(END, f"[-] {username} ({client_address}) se ha desconectado.\n")
		client_socket.close()
		clients_listbox.delete(clients_listbox.get(0, END).index(username)) # Eliminar de la lista visual
		del  clients[client_socket] # Remover el cliente de la lista

# Función para enviar mensaje a todos los clientes
def broadcast(message, log_area):
	log_area.insert(END, f"Enviando a todos: {message}\n")
	for client_socket  in  clients:
		client_socket.send(message.encode('utf-8'))
		
# Función para enviar mensaje a un cliente específico
def send_to_client(selected_username, message, log_area):
	for client_socket, client_username  in  clients.items():
		if  client_username  ==  selected_username:
			client_socket.send(message.encode('utf-8'))
			log_area.insert(END, f"Enviando a {selected_username}: {message}\n")
			break

# Función para iniciar el servidor
def start_server(log_area, clients_listbox):
	server  =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('0.0.0.0', 9999))
	server.listen(5)
	log_area.insert(END, "[*] Servidor escuchando en el puerto 9999\n")
	
	while  True:
		client_socket, client_address  =  server.accept()
		client_handler  =  threading.Thread(target=handle_client, args=(client_socket, client_address, log_area, clients_listbox))
		client_handler.start()

# Interfaz Gráfica con Tkinter
def create_server_interface():
	root  =  Tk()
	root.title("Servidor Multihilo")
	
	frame  =  Frame(root)
	frame.pack()
	
	# Área de log para mostrar los mensajes
	log_area  =  Text(frame, height=20, width=50)
	log_area.pack(side=LEFT)
	
	# Lista de clientes conectados
	clients_listbox  =  Listbox(frame, height=20, width=20)
	clients_listbox.pack(side=LEFT)
	
	# Área para escribir mensajes
	message_entry  =  Entry(frame, width=50)
	message_entry.pack()

	# Botón para enviar mensaje a todos
	broadcast_button  =  Button(frame, text="Enviar a todos", command=lambda: broadcast(message_entry.get(), log_area))
	broadcast_button.pack()
	
	# Botón para enviar mensaje a cliente seleccionado
	send_to_client_button  =  Button(frame, text="Enviar a cliente", command=lambda: send_to_client(clients_listbox.get(ACTIVE), message_entry.get(), log_area))
	send_to_client_button.pack()
	
	# Botón para iniciar el servidor
	start_button  =  Button(frame, text="Iniciar Servidor", command=lambda: threading.Thread(target=start_server, args=(log_area, clients_listbox)).start())
	start_button.pack()

	root.mainloop()

if  __name__  ==  "__main__":
create_server_interface()
```
### **Cliente**
```python
import  socket
import  threading
from  tkinter  import  *

# Función para enviar mensaje al servidor
def  send_message(client_socket, entry, log_area):
	message  =  entry.get()
	client_socket.send(message.encode('utf-8'))
	log_area.insert(END, f"Tú: {message}\n")
	entry.delete(0, END)

# Función para recibir mensajes del servidor
def  receive_messages(client_socket, log_area):
	while  True:
		try:
			message  =  client_socket.recv(1024).decode('utf-8')
			log_area.insert(END, f"Servidor: {message}\n")
		except ConnectionResetError:
			break

# Interfaz Gráfica para el Cliente
def  create_client_interface():
	root  =  Tk()
	root.title("Cliente TCP")

	frame  =  Frame(root)
	frame.pack()

	# Sección para el nombre de usuario
	label_username  =  Label(frame, text="Nombre de usuario:")
	label_username.pack()
	username_entry  =  Entry(frame, width=50)
	username_entry.pack()
	
	# Sección para los mensajes después de la conexión
	label_message  =  Label(frame, text="Escribe tu mensaje:")
	label_message.pack_forget() # Se oculta al inicio
	message_entry  =  Entry(frame, width=50)
	message_entry.pack_forget() # Se oculta al inicio
	
	log_area  =  Text(frame, height=10, width=50)
	log_area.pack()
	
	# Botón para enviar el mensaje
	send_button  =  Button(frame, text="Enviar", command=lambda: send_message(client_socket, message_entry, log_area))
	send_button.pack_forget() # Se oculta al inicio

	# Función para conectar al servidor
	def  connect_to_server():
		global  client_socket
		client_socket  =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(('192.168.43.96', 9999))
		
		# Enviar nombre de usuario al servidor
		username  =  username_entry.get()
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
	connect_button  =  Button(frame, text="Conectar", command=connect_to_server)
	connect_button.pack()

	root.mainloop()
  
if  __name__  ==  "__main__":
	create_client_interface()
```
## **Pruebas Realizadas**

1.  **Conexión de múltiples clientes:** Se probó que varios clientes puedan conectarse simultáneamente.
2.  **Envío de mensajes:** Se verificó el envío de mensajes tanto global como individualmente.
3.  **Manejo de desconexiones:** El servidor registra la desconexión de un cliente y lo elimina de la lista.
4.  **Interface gráfica:** Todos los botones y campos de texto funcionan correctamente.

## **Posibles Mejoras**

1.  **Autenticación de usuarios:** Implementar un sistema de login para mejorar la seguridad.
2.  **Encriptación de mensajes:** Usar TLS/SSL para proteger las comunicaciones.
3.  **Interfaz más moderna:** Actualizar la GUI con un framework como **PyQt** o **Kivy**.
4.  **Soporte a mensajes multimedia:** Permitir el envío de imágenes o archivos.

## **Conclusiones**

Este proyecto demuestra el uso de **sockets TCP** y **multihilos** en Python, proporcionando una experiencia práctica en la implementación de aplicaciones cliente-servidor con interfaces gráficas. La integración con **Tkinter** facilita la interacción del usuario, y el sistema es fácilmente extensible para nuevas funcionalidades.