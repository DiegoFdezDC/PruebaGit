import socket
import select
import sys
import random

IP = "127.0.0.1"
PUERTO = 8080

ID = str(random.randint(1, 1000))

# Creamos el socket TCP y nos conectamos al servidor
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((IP, PUERTO))

# Enviamos el identificador
socket_client.send(ID.encode())

name = input("¿Cual es tu nombre?")
print(f"\nAhora otrs usuarios te veran como :{name}. Escribe exit para desconectarte\n")

while True:

    listo_leer, _, _ = select.select([sys.stdin, socket_client], [], [])

    for sock in listo_leer:
        #igual que en el servidor
        if sock == socket_client:
            # Mensaje recibido del servidor
            response = socket_client.recv(1024).decode()
            if not response:
                # Si el mensaje está vacío, el servidor cerró la conexión
                print("\nEl servidor ha cerrado la conexión.")
                socket_client.close()
                sys.exit()
            print(response)
        else:
            # El usuario ha escrito algo y pulsado ENTER
            msg = sys.stdin.readline()  # como input(), pero no bloquea
            if msg == "exit":
                print("\nCerrando cliente.")
                socket_client.close()
                sys.exit()
            message = "[" + name + "]:" +msg
            # Enviamos el mensaje al servidor
            socket_client.send(message.encode())
