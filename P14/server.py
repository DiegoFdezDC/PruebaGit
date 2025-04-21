import socket
import select

PORT = 9999
IP = "0.0.0.0"  # dirección de broadcast

# Creamos socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reutilizar el IP y puerto
server_socket.bind((IP, PORT))
server_socket.listen()

print(f"\n[SERVER] Servidor escuchando en {IP}:{PORT}...")

sockets = [server_socket]
name_collection = ["Server"]  # Guardará los nombres

# Bucle principal
while True:
    listo_leer, _, _ = select.select(sockets, [], [])  # uso del select para gestionar los disponibles

    for sock in listo_leer:
        if sock == server_socket:
            # Aceptamos conexión y agregamos el socket a la lista
            client_socket, client_addr = server_socket.accept()
            sockets.append(client_socket)

            name = client_socket.recv(1024).decode()  # Recibimos el nombre del cliente
            name_collection.append(name)  # Guardamos el nombre en lugar del ID

            print(f"\n[SERVER] Se conectó un usuario con nombre: {name} desde {client_addr}")
            print(f"Usuarios Conectados: {name_collection}")

        else:
            try:
                # Obtenemos el mensaje
                response = sock.recv(1024).decode()
                indice = sockets.index(sock)

                # Si se manda una lista vacía interpretamos que se desconectó
                if not response:
                    print(f"\n[SERVER] Usuario: {name_collection[indice]} se desconectó")
                    sockets.pop(indice)
                    name_collection.pop(indice)
                    sock.close()

                # El mensaje lo reenviamos a todos menos al servidor y al que lo mandó
                elif response.startswith("["):
                    for cliente in sockets:
                        if cliente != server_socket and cliente != sock:
                            cliente.send(f"\n{response}".encode())
                # Si no empieza con [ es que es un mensaje privado
                elif response.startswith("/tell"):
					
                    busca = response.split(" ")
                    comando =busca [0]
                    destinatario = busca[1]
                    mensaje_privado = busca[2]
                    print(f"{busca[0]}")
                    print(f"{busca[1]}")
                    print(f"{busca[2]}")

                    print(f"Buscando a {destinatario}...")

                    if destinatario in name_collection:
                        indice_destinatario = name_collection.index(destinatario)
                        sockets[indice_destinatario].send(f"[Privado de {name_collection[indice]}]: {mensaje_privado}".encode())

            except Exception as e:
                print(f"Hubo un error: {e}, terminando el programa")
                exit()
