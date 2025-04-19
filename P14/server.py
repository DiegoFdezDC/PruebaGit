import socket
import select


PORT = 9999
IP = "0.0.0.0" #dijo Luis que mejor en la de broadcast
IDS = 0

#recuerda poner en los decode y encode "uft-8"

#Creamos socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reutilizar el IP y puerto
server_socket.bind((IP, PORT))
server_socket.listen()

print(f"\n[SERVER] Servidor escuchando en {IP}:{PORT}...")

sockets = [server_socket]
ID_collection = [IDS]  # Guarda los ID

# Bucle principal
while True:
    listo_leer, _, _ = select.select(sockets, [], [])  # uso del select para ir usando los que estén disponibles
    
    for sock in listo_leer:
		
        # Aquí vemos si alguien intenta iniciar sesión
        if sock == server_socket:

            #Aceptamos conexion y guardamos el socket en la lista de sockets
            client_socket, client_addr = server_socket.accept()
            sockets.append(client_socket)

            ID = client_socket.recv(1024).decode()
            
            #Agregamos el id a la coleccion
            ID_collection.append(ID)

            print(f"\n[SERVER] Se conecto un usuario con ID:{ID} desde {client_addr}")
            print(f"Usuarios Conectados: {ID_collection}")
        #Ahora vemos si hay clientes intentando mandar mensajes
        else:
            try:
                #Obtenemos el mensaje
                response = sock.recv(1024).decode()
                indice = sockets.index(sock)
                
                # si se manda una lista vacia interpretamos que se desconecto
                if not response:
                    print(f"\n[SERVER] USUARIO: {ID_collection[indice]} se desconecto")
                    # es mejor usar remove pq el pop tendríamos que recorrer las listas en busca de 1 igual
                    sockets.pop(indice)
                    ID_collection.pop(indice)
                    sock.close()
                    
				#El mensaje lo reenviamos a todos menos al servidor y al que lo mando
                else:
                    for cliente in sockets:
                        if cliente != server_socket and cliente != sock:
                            cliente.send(f"\n{response}".encode())

            except:
                print("Hubo un error, terminando el programa")
                exit()
