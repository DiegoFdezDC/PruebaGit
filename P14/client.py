import socket
import select
import sys

# Por comodidad pedimos que introduzca la IP 
IP = input("Introduzca la ip a la que desea conectarse\n")
if IP == "0":
	IP = "127.0.0.1"
PORT = 9999
conver = []

# Creamos el socket TCP y nos conectamos al servidor
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((IP, PORT))

name = input("[APP] ¿Cuál es tu nombre?\n")

# Enviamos el nombre
socket_client.send(name.encode())

print("[APP] Escribe 'help' para ver más comandos")
print(f"\n[APP] Bienvenido al chat grupal, {name}\n")

while True:

    listo_leer, _, _ = select.select([sys.stdin, socket_client], [], [])

    for sock in listo_leer:
        if sock == socket_client:
            # Mensaje recibido del servidor
            response = socket_client.recv(1024).decode()
            if not response:
                # Si el mensaje está vacío, el servidor cerró la conexión
                print("\n[APP] El servidor ha cerrado la conexión.")
                socket_client.close()
                exit()
            print(response)
            conver.append(response)

        else:
            # El usuario ha escrito algo y pulsado ENTER
            msg = sys.stdin.readline().strip()  # como input(), pero no bloquea
            
            if msg == "exit":
                print("\n[APP] Saliendo de la aplicación... ")
                socket_client.close()
                exit()

            elif msg == "save":
                with open(f"Chat_de_{name}.txt", "w") as archivo:
                    archivo.write(f"Conversación de {name}\n")
                    for coms in conver:
                        archivo.write(f"{coms}\n")
                print("[APP] Archivo guardado con éxito")
                print("==================================")

            elif msg == "help":
                print("[APP] Escribe 'exit' para desconectarte")
                print("[APP] Escribe 'save' para guardar la conversación")
                print("[APP] Usa '/tell <destinatario> <mensaje>' para enviar un mensaje privado")
            
            elif msg.startswith("/tell"):
                # Formato de mensajes privados: /tell <destinatario> <mensaje>
                priv = msg.split(" ", 2)  # Dividimos en tres partes: comando, destinatario y mensaje
                if len(priv) == 3:
                    destinatario = priv[1]
                    mensaje_privado = priv[2]
                    # Enviamos al servidor en formato: destinatario mensaje
                    socket_client.send(f"/tell {destinatario} {mensaje_privado}".encode())
                else:
                    print("[APP] Formato incorrecto. Usa: /tell <destinatario> <mensaje>")
            
            else:
                # Mensaje normal al chat grupal
                message = f"[{name}]: {msg}"
                conver.append(message)
                # Enviamos el mensaje al servidor
                socket_client.send(message.encode())
