import socket
import select
import sys
import random


IP = f"127.0.0.{str(random.randint(1,200))}"
PORT = 9999

ID = str(random.randint(1, 5000))

# Creamos el socket TCP y nos conectamos al servidor
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((IP, PORT))

# Enviamos el identificador
socket_client.send(ID.encode())
conver = []


name = input("[APP] ¿Cual es tu nombre?\n")
print("[APP] Escribe help para ver mas comandos")
print(f"\n[APP] Bienvenido al chat grupal {name} \n")

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
                print("\n[APP] Saliendo de la aplicacion... ")
                socket_client.close()
                sys.exit()
                
            elif msg == "save\n":
                with open(f"Chat_de_{name}.txt","w") as archivo:
                    archivo.write(f"Conversacion de {name}\n")
                    for coms in conver:#Resumen
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
