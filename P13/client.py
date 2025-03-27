import socket
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
CLIENT_IP = "127.0.0.2"
CLIENT_PORT = 8000
NOMBRES_REGIS = ["APP","SERVER","exit"]

#Creacion socket "escucha" UDP de recepcion para el cliente
while True:
	try:
	sserver_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sserver_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sserver_UDP.bind((CLIENT_IP,CLIENT_PORT))
	break
	
	except OSError as noconex
		if noconex.errno == 98:
			
			CLIENT_PORT += CLIENT_PORT
			
			partesIP = CLIENT_IP.split(".")
			ultimoIP = int(partesIP[3])
			ultimoIP = += 1
			partesIP[3] = str(ultimoIP)
			IP_CLIENTE = ".".join(partesIP)
		else
		print(f"[ERROR] No se pudo crear el socket escucha UDP.")
		sserver_UDP.close()
		exit()
		
print(f"[APP]Escuchando mensajes de otros usuarios en: {CLIENT_IP}:{CLIENT_PORT}")

#Creacion socket TCP para la conexion con el servidor
try:
    print(f"[APP]: Conectando al servidor {SERVER_HOST}:{SERVER_HOST}...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[APP]: Conexión establecida.")

    
except ConnectionRefusedError:
    print(f"[ERROR] No se pudo conectar al servidor TCP {SERVER_HOST}:{SERVER_PORT}.")
    client_socket.close()
    exit()

#Tomar los datos de conexion name del usuario y le mandamos los datos al Server para confirmar
while True:
    name = input("[APP]Elija un nombre de usuario\n")
    if ',' not in name:
        if name not in NOMBRES_REGIS:
            #Mandamos al Server el mensaje inicial
            iniciosesion = ",".join("0",name, CLIENT_IP, str(UDP_PORT))
            client_socket.sendall(iniciosesion.encode())

            #Espereamos la confirmacion del Servidor
            conf_inicio = client_socket.recv(1024).decode()
            conf_inicio_partes = conf_inicio.split(",")
            #Todo bien
            if conf_inicio_partes[0] == "0":
                print("[APP]Perfecto su nombre fue registrado correctamente")
                break 
        else:  
            print("[APP]Lo sentimos el nombre introducido ya esta registrado")
       
    else:
        print("[APP]Introduzca un nombre sin: ,")
        
        
#Decidimos la siguiente accion del usuario
while True:
    decision = input("[APP]Que desea hacer? \n 1 => Conectarse a un usuario\n 2 => Ver la lista de usuarios conectados  \n 3 => salir del programa \n")
    #Solicitar la lista de usuarios
    if decision == "2":
        accion = ",".join("2","_","_","_")
        lista = client_socket.recv(1024).decode() #Aqui el server que no mande flag
        print(f"[APP]{lista}")
        
    #Solicitar conexion
    elif decision == "1":
        while True:
            friend = input("[APP]Con quien quieres hablar?, pulse escriba si quiere cerrar sesion \n")
            
            if friend == "exit":
                print("[APP]Saliendo de la seleccion de chat...")
                break
            
            elif friend == name:
                print("[APP]No eres tu propio amigo buscate otro a quien llamar")
                
            elif ',' in friend:
                print("[APP]Introduzca el nombre del usuario sin ,")
                
            #Todo bien
            else:
            accion = ",".join("1",friend,"_","_")
            client_socket.sendall(accion.encode())
    
            conf_friend = client_socket.recv(1024).decode()
            conf_friend_partes = conf_friend.split(",")
            
            if conf_friend_partes[0] == "1":
                print("[APP]El usuario seleccionado no se encuentra disponible o no existe")
                break
            #Ya en este punto empezaria la conexion p2p
            print(f"[APP]Conexion realizada con exito, para hablar con otro usuario introduzca: exit")
#~~~~~~~~~~~~~~~Maybe esto deberia ir dentro del bucle
            sclient_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sclient_UDP.settimeout(3)
            while True:
                msg = input(f"[{name}]")
                if msg == "exit":
                    sclient_UDP.close()
                    break
                else:
                    message = "[{name}]" + msg
                    sclient_UDP.sendto(message.encode(),(conf_friend[2],int(conf_friend[3])))
    #Salir del programa
    elif decision == "3":
        sserver_UDP.close()
        client_socket.close()
        break
            
            

#Estructura mensajes cliente -> servidor [flag,name,ip,port_udp]
#   flag:
#       flag == 0 => Inicio de sesion
#       flag == 1 => Buscar amigo 
#       flag == 2 => Solicitar lista
#   name:
#       flag = 0 => name ==> propio del cliente
#       flag = 1 => name ==> del amigo que busca
#       flag = 2 => name ==> puede ir vacio o con tu nombre
#   ip: La ip propia o vacia salvo en flag => 0 que siempre la propia
#   port_udp: El propio o vacio salvo en flag => 0 que siempre el propio

#Estructura mensajes servidor -> cliente [flag,name,ip,port_udp]
#   flag:
#       flag => 0 => Peticion Aceptada
#       flag => 1 => Peticion Denegada
#           Si se deniega una peticion el resto de campos => vacios         
#   name:
#       Peticion = Inicio Sesion => name ==> vacio
#       Peticion = Buscar amigo => name ==> name del amigo
#       Peticion = Solicitar Lista => name ==> lista de conectados
#   ip y puerto_udp:
#       Peticion = Inicio Sesion => ip y puerto_udp ==> vacio
#       Peticion = Buscar amigo => ip y puerto_udp ==> ip y puerto_udp del amigo
#       Peticion = Solicitar Lista => ip y puerto_udp ==> vacio
