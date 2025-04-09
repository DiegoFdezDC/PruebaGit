#***************
#PRACTCA1.3
#***************

import socket
import select

PUERTO=8080
IP="127.0.0.1"
BUFFSIZE= 1024

#En este programa se hace especial uso en select.select ya que usamos dos sockets


#CREACION DEL SOCKET SERVIDOR
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #perimite reutilizar el IP  y puerto
server_socket.bind((IP, PUERTO))
server_socket.listen()

print(f"\nServidor escuchando en {IP}:{PUERTO}...")

socket_activos=[server_socket]  #lista para sockets aqtivos para escuchar
client_nombre={}   #para guardar los nombres del cliente que esté conectado

while 1:
    socket_listo_leer, _, _= select.select(socket_activos, [], [])  #uso del select para ir usando los que esten disponibles

    for socket_i in socket_listo_leer:
        #socket_i es variable para recorrer todos los guardados en listo_usar
        #usamos este socket poq querermos los que tengan datos disponibles para ser leidos
        #este socket incluye los conectados pero solo los que tienen algo que enviar
        if socket_i==server_socket: #si al recorrer la lista de sockets coincide con el servidor...

            client_socket, client_addr=server_socket.accept()   #aceptamos conexion y guardamos info del cliente
            client_socket.send("\nEscriba su nombre: ".encode())    #envia peticion de nombre al cliente
            nombre=client_socket.recv(BUFFSIZE).decode().strip() #recibe el nomrbe
            socket_activos.append(client_socket)    #guardamos el socket del cliente en la lista de los activos
            client_nombre[client_socket]=nombre  #guardamos el nombre en la lista con el socket asociado
            print(f"\n** {nombre} conectado desde {client_addr}")

        else:   #si al recorrer la lista le toca un cliente...

            try:
                mensaje_recibido=socket_i.recv(BUFFSIZE).decode().strip()  #RECIBE MENSAJE
                if mensaje_recibido:    #si recibe contenido...
                    nombre=client_nombre[socket_i]  #guardamos el nombre del que acaba de enviar el mensaje
                    print(f"\nMensaje de {nombre}")
                    for socket_j in socket_activos:
                        #usamos sockets_activos pq queremos que recorra todos ellos y les haga un send de la info que hemos recibido
                        if socket_j != server_socket and socket_j != socket_i:
                            #con este for recorremos todos los sockets que no sean ni servidor ni el remitente del mensaje
                            #y si no son ellos, se les envia el mensaje
                            socket_j.send(f"\n{nombre}: {mensaje_recibido}".encode())

                else:   #si mensaje viene vacio, se asume que el cliente quiere desconectarse
                    print(f"\n**{client_nombre[socket_i]} DESCONECTADO**")
                    socket_activos.remove(socket_i) #eliminamos el socjet de activos
                    socket_i.close()    #cerramos este socket que recorria el bucle for
                    del client_nombre[socket_i] #eliminamos el socket de los clientes

            except:
                socket_activos.remove(socket_i)
                socket_i.close()
                del client_nombre[socket_i]
