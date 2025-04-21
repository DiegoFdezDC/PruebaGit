import socket
import select

PORT = 9999
IP = "0.0.0.0"  # dijo Luis que mejor en la de broadcast
IDS = 0

# Recuerda poner en los decode y encode "utf-8"

# Creamos socket TCP
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

            # Aceptamos conexión y guardamos el socket en la lista de sockets
            client_socket, client_addr = server_socket.accept()
            sockets.append(client_socket)

            ID = client_socket.recv(1024).decode()

            # Agregamos el id a la colección
            ID_collection.append(ID)

            print(f"\n[SERVER] SE conectó un usuario con ID:{ID} desde {client_addr}")
            print(f"Usuarios Conectados: {ID_collection}")

        # Ahora vemos si hay clientes intentando mandar mensajes
        else:
            try:
                # Obtenemos el mensaje
                response = sock.recv(1024).decode()
                indice = sockets.index(sock)

                # Si se manda una lista vacía interpretamos que se desconectó
                if not response:
                    print(f"\n[SERVER] USUARIO: {ID_collection[indice]} se desconectó")
                    sockets.pop(indice)
                    ID_collection.pop(indice)
                    sock.close()

                # El mensaje lo reenviamos a todos menos al servidor y al que lo mandó
                elif response.startswith("["):
                    for cliente in sockets:
                        if cliente != server_socket and cliente != sock:
                            cliente.send(f"\n{response}".encode())
                # Si no empieza con [ es que es un mensaje privado
                else:
                    busca = response.split(" ", 2)  # Ajustamos el split para que divida correctamente
                    destinatario = busca[1]
                    mensaje_privado = busca[2]

                    print(f"Buscando {destinatario}...")

                    if destinatario in ID_collection:
                        indice_destinatario = ID_collection.index(destinatario)
                        sockets[indice_destinatario].send(f"[Privado de {ID_collection[indice]}]: {mensaje_privado}".encode())

            except Exception as e:
                print(f"Hubo un error: {e}, terminando el programa")
                exit()

