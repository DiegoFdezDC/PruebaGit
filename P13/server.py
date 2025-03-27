import socket #libreria de sockets
import select #libreria de select

DIR_IP = "127.0.0.1" #aqui a pesar de que conviene la 0.0.0.0 ponemos la que esta para hacer las pruebas
PUERTO = 9999 # definimos aqui el puerto de servidor por el mismo motivo que el anterior

socketSERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creamos el socket de Servidor en TCP     
socketSERVIDOR.bind((DIR_IP, PUERTO))# Al socket del servidor TCP le adjudicamos el puerto e ip definidas anteriormente
socketSERVIDOR.listen(5)#ponemos el socket en modo escucha por el puerto que le hemos adjudicado antes
usuario = [] # creamos una lista bacia en la que recopilaremos los nombres identificadores de los usuarios que se conecten
"""
#a pesar de que ya no la vayamos a usar comento adicionalmente la clase datos
class datos:#definimos la clase datos, esto es una plantilla que se usara para tratar a los datos como objetos
    def __init__(info, nombre, ip, puerto_udp, puerto_tcp): #defino el metodo __init__, este metodo es un metodo especial constructor que se ejecuta automaticamente cada vez que se crea una instancia de una clase ("nuevo dato"),este lo que hace es tambien inicializar los tributos que definiremos abajo
        info.nombre = nombre #primer argumento del metodo, en este argumento guardaremos el nombre del usuario que se conecte
        info.ip = ip#segundo argumento del metodo, en este argumento guardaremos la i`p del usuario que se conecte
        info.puerto_udp = puerto_udp#tercer argumento del metodo, en este argumento guardaremos el puerto UDP del usuario que se conecte
        info.puerto_tcp = puerto_tcp#cuarto y ultimo argumento del metodo, en este argumento guardaremos el puerto TCP del usuario que se conecte"""

while True:#Bucle en el que estaremos buscando la gente que quiera conectarse
    conectados = len(usuario)#variable que almecena el tamaño de usuarios que se han conectado al servidor, se actualiza constantemente
    
    listaLEER, _, _ = select.select([socketSERVIDOR], [], []) #almacenamos en listaLEER los sockets que esten preparados para ser leidos sin editar, utilizamos la funcion select para ello
    #la funcion select devuelve 3 valores (de los cuales solo nos interesa el 1), el primero que ya hemos comentado, el 2 es una lista con los sockets que estan preparados para que se les escriabn datos 
    #y el 3 es una lista de sockets que han tenido alguna clase de problemas
    
    if socketSERVIDOR in listaLEER: #comprobamos si el socket se encuentra preparado para su lectura
        scliente, IP_CLIENTE = socketSERVIDOR.accept()  # De aquí se obtiene la IP del cliente
        
        peticion = socketCLIENTE.recv(1024).decode() #aqui obtenemos la peticion que manda el cliente 
        peticion_partes = peticion.split(",")   # Separamos dicha peticion en pequeños trozos, cliente manda: "flag,name,IP,Puerto_UDP" como "estructura" de mensaje
        #sabiendo que el primer campo de la peticion es lo que quiere hacer el usuario, hacemos un caso para cada condicion
        #Inicio Sesion
        if peticion_partes[0] == "0": #el primer caso es el inicio de sesion obligatorio dnd el usuario pasa su nombre identificador, su puerto udp entre otros valores que definimos anteriormente
            if conectados == 0: #comprobamos que no haya conectados en ese caso el registro del usuario seria inmediato
                """ de la misma forma que la definicion de la clase esto ya no se utiliza
                aceptado = datos(peticion_partes[1],peticion_partes[2],peticion_partes[3],IP_CLIENTE)#almacenamos en una variable de tipo datos la informacion llegada del inicio de conexion"""
               
               
                scliente.sendall("0")#mandamos el codigo de que todo fue bien como respuesta al cliente, esots codigos vienen definidos abajo
            else:#en caso de que haya algun usuario ya registrado debemos comprobar si sus nombres(que fucionan como identificadores) no coincidan
                repetido = False#inicializamos la variable booleana que nos servira para comprobar si hay algun repe
                for a in range(conectados):#aqui utilizamos un bucle para recorrer la lista de conectados
                    if usuario[a].nombre == dato.nombre:# esto ya no se puede hacer al no poder utilizar POO, vamos verificar si el identificador del recien llegado coincide con el de alguno que ya este registrado
                        repetido = True # si coincide cambiamos el valor del booleano a true  
                        break #terminamos la busqueda pq ya sabemos que ya coincide con 1 asiq no puede registrarse
                if repetido == False:#si no se ha activado repetido cm true esq no hay repes asiq todo bien
                    #Guardamos name,ip,Puerto_UDP, Puerto_TCP
                    aceptado = datos("0",peticion_partes[1],peticion_partes[2],peticion_partes[3],IP_CLIENTE)
                    #Realizamos el registro en la matriz usuario[] para acceder a los datos podemos hacer print(usuario[n].nombre)
                    usuario.append(aceptado)#se guardaria en usuario el valor de los datos recogids
                    
                    scliente.sendall("0")#mansamos el codigo de que todo bien
                else:#de lo contrario significa que ya hay alguien con ese identificador
                    scliente.sendall("1")#mandamos el codigo de que ya hay un usuario registrado cn ese nombre
                    
        #Buscar un amigo
        elif peticion_partes[0] == "1":#aqui llega el codigo de la flag para que busquemos a un amigo con el que conectarse
            repetido = False#realizamos el mismo concepto de busqueda que en el inicio de sesion
            for a in range(conectados):#repasamos la matriz de tamaño conectados
                if usuario[a].nombre == peticion_partes[1]:#si coincide el valor que busca el usuario con alguno que se encuentre en la matriz
                    amigo = ",".join("0",usuario[a].nombre,usuario[a].ip,usuario[a].puerto_udp)#ese usuario lo guardamos en una variable llamada amigo junto con sus datos de acceso udp y el identificacion de que el proceso fue realizado con exito
                    repetido = True# detenemos el bucle y cambiamos el valor del booleano puesto que ya no hace falta buscar mas
                    break#detenemos el bucle
            if repetido == True:#verificamos si encontro en el bucle uno repetido
                scliente.sendall(amigo)#una vez confirmado mandamos mediante el protocolo tcp los datos que tenemos sobre dicho usuario
            else:#si repetido no cambio
                scliente.sendall("1")#mandamos el flag de que algo fallo o que no encontro a la persona que buscaba

        #Solicita Lista de conectados
        elif peticion_partes[0] == "2":#nuevo caso en esta situacion lo que quiere saber la otra parte es los nombres de los usuarios ya registrados en el servidor
            for a in range(conectados):#recorremos la lista de conectados
                scliente.sendall(usuario[a].nombre)#le mandamos los nombres de los usuarios conectados al cliente



        
        
        
        
        
               
        


