import socket
import select


PORT = 8080
IP = "127.0.0.1"
IDS = 0
# En este programa se hace especial uso en select.select ya que usamos dos sockets


# CREACION DEL SOCKET SERVIDOR
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reutilizar el IP y puerto
server_socket.bind((IP, PORT))
server_socket.listen()

print(f"\nServidor escuchando en {IP}:{PORT}...")

sockets = [server_socket]
ID_collection = [IDS]  # para guardar los ID
repetido = 0
list = ["server"] #guarda los datos del nombre para que no haya repes
# Bucle principal
while True:
    listo_leer, _, _ = select.select(sockets, [], [])  # uso del select para ir usando los que estén disponibles

    for sock in listo_leer:

        # Aquí vemos si alguien intenta iniciar sesión
        if sock == server_socket:

            # aceptamos conexión y guardamos el socket en la lista de sockets
            client_socket, client_addr = server_socket.accept()
            sockets.append(client_socket)

            ID = client_socket.recv(1024).decode()
            
            # agregamos el id a la colección de identificaciones
            ID_collection.append(ID)

            name = client_socket.recv(1024).decode()
            while True:
                if name not in list:
                    client_socket.send(str(repetido).encode())
                    break
                repetido = repetido + 1
                name = name + str(repetido)
                
            list.append(name)
            print(f"\nel usuario con {ID} se conecto desde {client_addr}")

        # Ahora vemos si hay clientes intentando mandar mensajes
        else:
            try:
                #Obtenemos el mensaje
                response = sock.recv(1024).decode()
                indice = sockets.index(sock)
                
                # si se manda una lista vacia interpretamos que se desconecto
                if not response:
                    print(f"\nUSUARIO: {ID_collection[indice]} Perdió la conexión")
                    # es mejor usar remove pq el pop tendríamos que recorrer las listas en busca de 1 igual
                    sockets.pop(indice)
                    ID_collection.pop(indice)
                    list.pop(indice)
                    sock.close()
                    

                else:
                    for cliente in sockets:
                        if cliente != server_socket and cliente != sock:
                            cliente.send(f"\n{response}".encode())

            except:
                print("Hubo un error, terminando el programa")
                exit()
