import socket
import select
import sys
import random


IP = f"127.0.0.{str(random.randint(1,200))}"
PUERTO = 9999

conver = []
ID = str(random.randint(1, 1000))

# Creamos el socket TCP y nos conectamos al servidor
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((IP, PUERTO))

# Enviamos el identificador
socket_client.send(ID.encode())

name = input("[APP]¿Cual es tu nombre?\n")
socket_client.send(name.encode())
repe = socket_client.recv(1024).decode()
if repe != "0":
    name = name + repe




print("[APP] nombre registrado con exito, escribe help para ver mas comandos")
print(f"\n[APP] BIen venido al chat grupal {name} \n")

while True:

    listo_leer, _, _ = select.select([sys.stdin, socket_client], [], [])

    for sock in listo_leer:
        #igual que en el servidor
        if sock == socket_client:
            # Mensaje recibido del servidor
            response = socket_client.recv(1024).decode()
            if not response:
                
                # Si el mensaje está vacío, el servidor cerró la conexión
                print("\n[APP] El servidor ha cerrado la conexión.")
                socket_client.close()
                sys.exit()
            print(response)
            conver.append(response)
            
        else:
            # El usuario ha escrito algo y pulsado ENTER
            msg = sys.stdin.readline()  # como input(), pero no bloquea
            if msg == "exit\n":
                print("\n[APP]Cerrando cliente.")
                socket_client.close()
                sys.exit()
                
            elif msg == "save\n":
                with open(f"Chat_{name}.txt","w") as archivo:
                    archivo.write(f"Conversacion de {name}\n")
                    for coms in conver:#
                        archivo.write(f"{coms}")
                    
                print("[APP] Archivo guardado con exito")
                print("==================================")
                
            elif msg == "help\n":
                print("[APP] Escribe exit para desconectarte")
                print("[APP] Escribe save para guardar la conversacion")
                

            message = "[" + name + "]:" +msg
            conver.append(message)
            # Enviamos el mensaje al servidor
            socket_client.send(message.encode())
