import socket
import select

DIR_IP = "127.0.0.1"#aqui dijo de definirlo en el 0.0.0.0
PUERTO = 9999
flag=0
i=0

socketSERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Servidor en TCP
socketSERVIDOR.bind((DIR_IP, PUERTO))
socketSERVIDOR.listen(5)                                                # El servidor escucha por esa dir. y puerto 
usuario = []
class datos:
    def __init__(info, nombre, ip, puerto_udp, puerto_tcp):
        info.nombre = nombre
        info.ip = ip
        info.puerto_udp = puerto_udp
        info.puerto_tcp = puerto_tcp
while True:
    conectados = len(usuario)
    listaLEER, _, _ = select.select([socketSERVIDOR], [], [])
    
    if socketSERVIDOR in listaLEER:
        scliente, IP_CLIENTE = socketSERVIDOR.accept()  # De aquí se obtiene la IP del cliente
        
        peticion = socketCLIENTE.recv(1024).decode()
        peticion_partes = peticion.split(",")   # El cliente manda: "flag,name,IP,Puerto_UDP"
    
        #Inicio Sesion
        if peticion_partes[0] == "0":
            if conectados == 0:
                #Guardamos name,ip,Puerto_UDP, Puerto_TCP
                aceptado = datos(peticion_partes[1],peticion_partes[2],peticion_partes[3],IP_CLIENTE)
                #Realizamos el registro en la matriz usuario[] para acceder a los datos podemos hacer print(usuario[n].nombre)
                usuario.append(aceptado)
                #mansamos el codigo de que todo bien
                scliente.sendall("0")
            else:
                repetido = False
                for a in range(conectados):
                    if usuario[a].nombre == peticion_partes[1]:
                        repetido = True 
                        break
                if repetido == False:
                    #Guardamos name,ip,Puerto_UDP, Puerto_TCP
                    aceptado = datos("0",peticion_partes[1],peticion_partes[2],peticion_partes[3],IP_CLIENTE)
                    #Realizamos el registro en la matriz usuario[] para acceder a los datos podemos hacer print(usuario[n].nombre)
                    usuario.append(aceptado)
                    #mansamos el codigo de que todo bien
                    scliente.sendall("0")
                else:
                    scliente.sendall("1")
                    
        #Buscar un amigo
        elif peticion_partes[0] == "1":
            repetido = False
            for a in range(conectados):
                if usuario[a].nombre == peticion_partes[1]:
                    amigo = ",".join("0",usuario[a].nombre,usuario[a].ip,usuario[a].puerto_udp)
                    repetido = True
                    break
            if repetido == True:
                scliente.sendall(amigo)
            else:
                scliente.sendall("1")

        #Solicita Lista de conectados
        elif peticion_partes[0] == "2":
            for a in range(conectados):
                scliente.sendall(usuario[a].nombre)



        
        
        
        
        
               
        


