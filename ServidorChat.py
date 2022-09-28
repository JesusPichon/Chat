import socket   
import threading
import sys

print("Servidor listo")

#Guarda los datos de los clientes 
clientes = []
nombreUsuarios = []

#Revisa si existe el usuario dentro del arreglo 
def existeUsuarioTCP(_nombre):
    for nombre in nombreUsuarios:
        if(nombre == _nombre):
            return True

#host y canal de comunicacion  TCP
host = '172.31.0.224'
puertoTCP = 55555

#exclusion del mensaje TCP para el cliente que lo envia 
def broadcast(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)

#manejador de mensajes TCP-
def handle_messages(cliente):
    while True:
        try:
            #se recibe un nombre de usuario
            #si se toco la opción de mandar mensaje a todos, va a verificar
            #con el mensaje enviado
            mensaje = cliente.recv(1024)
            #busca al usuario
            if(existeUsuarioTCP(mensaje.decode())):
                index = nombreUsuarios.index(mensaje.decode())
                clienteUsuario = clientes[index]

                dataM = cliente.recv(1024)
                clienteUsuario.send(dataM)
            else:
                broadcast(mensaje, cliente)
        except:
            index = clientes.index(cliente)
            nombreUsuario = nombreUsuarios[index]
            broadcast(f"ChatBot: {nombreUsuario} se desconecto".encode('utf-8'), cliente)
            clientes.remove(cliente)
            nombreUsuarios.remove(nombreUsuario)
            cliente.close()
            break


def recibe_conexionesTCP():
    #creacion del socket TCP
    try:
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTCP.bind((host, puertoTCP))
        socketTCP.listen()
        print(f"Canal de  comunicacion TCP corriendo en {host}:{puertoTCP}")
    except socket.error as msg:
        print ('fallo al crear el socket. código de error : ' + str(msg[0]) + ' Mensaje ' + msg[1])
        socketTCP.close
        sys.exit()
        
        

    #ciclo que mantine la conexion con nuevos y diferentes usuarios TCP
    while True:
        #se acepta la conexión
        cliente, direccion = socketTCP.accept()
        #se envía un mensaje para solicitar el nombre de usuario
        cliente.send("@nombreUsuario".encode("utf-8"))
        #se recibe el nombre de usuario
        nombreUsuario = cliente.recv(1024).decode('utf-8')
        #se agrega  el cliente  a un arreglo de clientes
        clientes.append(cliente)
        #se agrega el nombre de usuario a un arreglo para hacer la búsqueda al 
        #querer mandar un mensaje a un usuario concreto
        nombreUsuarios.append(nombreUsuario)
        print(f"{nombreUsuario} esta conectado por el canal TCP con: {str(direccion)}")
       
        #envio de la lista de usuarios conectados a todos los usuarios
        listaNombres = "ChatBot:,"
        for nom in nombreUsuarios:
            listaNombres = listaNombres + nom +','

        #se envía la lista a los usuarios excepto este
        broadcast(listaNombres.encode("utf-8"),cliente)
        #se envía la lista de los usuarios activos al usuario
        #que acaba de conectarse
        cliente.send(listaNombres.encode("utf-8"))
        #se inicia el manejador de mensajes
        thread = threading.Thread(target=handle_messages, args=(cliente,))
        thread.start()

#excluye el mensaje 
def broadcastUDP(mensaje, direccion, sUDP):
    for client in clientesUDP:
        if(client != direccion):
            sUDP.sendto(mensaje, client) 

 
#listas para guardar los clientes UDP
clientesUDP = []
nombreUsuariosUDP = []

#Revisa si existe el usuario dentro del arreglo 
def existeUsuario(_nombre):
    for nombre in nombreUsuariosUDP:
        if(nombre == _nombre):
            return True

#Puerto
puertoUDP = 10000
canalUDP = (host, puertoUDP)

def recibe_conexionesUDP():
    
    #crear el canal de comunicacion
    try:
        socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print ('fallo al crear el socket. código de error : ' + str(msg[0]) + ' Mensaje ' + msg[1])
        sys.exit()
    #crear la conexion 
    try:
        #se asigna el puerto y manda mensaje de que la conexion se creo con exito 
       socketUDP.bind((host, puertoUDP))
       print(f"Canal de comunicacion UDP corriendo en {host}:{puertoUDP}")
    except socket.error as msg:
        print ('Bind failed. Código de error : ' + str(msg[0]) + ' Mensaje ' + msg[1])
        sys.exit()

    while True:
        data, dir1 = socketUDP.recvfrom(4096) 

        if(data.decode() == "listo"):
            
            socketUDP.sendto("@nombreUsuario".encode("utf-8"), dir1)

            #obtenemos la direccion y el nombre de usuario que manda los mensajes 
            cliente, dir = socketUDP.recvfrom(4096) 
            nombreUsuario = cliente.decode()

            #guarda los nombres de usuario y los datos de los clientes 
            clientesUDP.append(dir)
            nombreUsuariosUDP.append(nombreUsuario)

            print(f"{nombreUsuario} esta conectado por el canal UDP con: {str(dir)}") 
            #mensaje = f"ChatBot: {nombreUsuario} se unio al chat!".encode("utf-8")

            listaNombres = "ChatBot:,"
            for nom in nombreUsuariosUDP:
                listaNombres = listaNombres + nom +','

            broadcastUDP(listaNombres.encode("utf-8"),dir,socketUDP)

            socketUDP.sendto(listaNombres.encode("utf-8") , dir)

        elif existeUsuario(data.decode()):

            index = nombreUsuariosUDP.index(data.decode())
            dirUsuario = clientesUDP[index]

            #socketUDP.sendto(data, dirUsuario)
            
            dtaUser= socketUDP.recv(4096)
            socketUDP.sendto(dtaUser,dirUsuario)
        else:
            broadcastUDP(data, dir1, socketUDP)
            
canalUDP = threading.Thread(target=recibe_conexionesUDP)
canalTCP = threading.Thread(target=recibe_conexionesTCP)

canalUDP.start()
canalTCP.start()
canalUDP.join()
canalTCP.join()


