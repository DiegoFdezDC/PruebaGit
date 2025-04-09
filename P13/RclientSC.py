#*************
#PRACTICA 1.3
#*************

#EN este cliente implementamos como nuevo la libreria sys, basicmente como el input pero no bloquea el programa
#Como select.select se le puede introducir mas cosas a parte de los sockets como siempre, he introducido sys.stdin
#AL incluirlo, podemos obtener dos resultados, el cliente recibe info del socket o bien envia info usando el sys


import socket
import select
import sys


IP = "127.0.0.1"
PUERTO = 8080
BUFFSIZE = 1024

# Creamos el socket TCP y nos conectamos al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP, PUERTO))

# El servidor nos pedirá el nombre al conectarnos
pregunta = cliente.recv(BUFFSIZE).decode()
print(pregunta)

# Enviamos el nombre al servidor
mi_nombre = input(">> ").strip()
cliente.send(mi_nombre.encode())

print(f"\nConectado como {mi_nombre}. Escribe 'exit' para salir.\n")

while True:
    # select.select() espera que suceda algo:
    #o bien el usuario escribe (sys.stdin)
    #o bien el servidor nos envía algo (cliente)
    ready_to_read, _, _ = select.select([sys.stdin, cliente], [], [])

    for fuente in ready_to_read:
        if fuente == cliente:
            #Mensaje recibido del servidor
            mensaje = cliente.recv(BUFFSIZE).decode()
            if not mensaje:
                # Si el mensaje está vacío, el servidor cerró la conexión
                print("\nEl servidor ha cerrado la conexión.")
                cliente.close()
                sys.exit()
            print(mensaje)
        else:
            #El usuario ha escrito algo y pulsado ENTER
            texto = sys.stdin.readline().strip()  # como input(), pero no bloquea
            if texto.lower() == "exit":
                print("\nCerrando cliente.")
                cliente.close()
                sys.exit()
            # Enviamos el mensaje al servidor
            cliente.send(texto.encode())
