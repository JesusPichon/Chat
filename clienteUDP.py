from tkinter import *
import socket
import threading
import tkinter

host = '172.31.0.224'
puerto = 10000
estado = 0

# Create a UDP socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#crear la dupla
server_address = (host, puerto)
#manda mensaje al servidor cuando esta listo 
cliente.sendto("listo".encode("utf-8"), server_address)

def recibir_mensajes():
    while True:
        try:
            #recibe el mensaje 
            mensaje = cliente.recv(1024).decode()

            if mensaje == "@nombreUsuario":
                cliente.sendto((nombreUsuario.get()).encode("utf-8"), server_address)

            elif(mensaje[:8] == "ChatBot:"):
                lista = mensaje.split(sep=',')
                n = listaConectados.size()
                listaConectados.delete(0,n)

                for i in lista:
                    listaConectados.insert(END,i) 

                listaConectados.delete(0) 
            #se recibió un mensaje 
            else:
                textChat.insert(tkinter.INSERT, mensaje)
                textChat.insert(tkinter.INSERT, "\n")
        except:
            print("Ops ha ocurrido un error")
            cliente.close
            break

def escribe_mensaje():
    data = f"{nombreUsuario.get()}: {varEnviar.get()}"
    cliente.sendto(data.encode("utf-8"), server_address)

def escribeMensajeUsuario():
    if(listaConectados.get(ANCHOR) != ""):
     print ("destino=",listaConectados.get(ANCHOR),sep="")
     data = f"{listaConectados.get(ANCHOR)}"
     cliente.sendto(data.encode("utf-8"), server_address)
     escribe_mensaje()


def iniciarHilos():
    global estado 
    #verifica que no se haya conectado antes
    #El campo de nombre no puede ser vacio
    if (nombreUsuario.get()!="" and estado == 0):
        estado=1
        recibe_hilo = threading.Thread(target=recibir_mensajes)
        recibe_hilo.start()
    

#ventana del cliente 
win = tkinter.Tk()  
win.title('Cliente UDP')
win.config(bg="#BBDEFB")


#interfaz grafica
etiquetaUsuario = tkinter.Label(win, text="Nombre del Usuario:",font=("Arial",9)).grid(row=0, column=0)
nombreUsuario = tkinter.Variable()
entradaUsuario = tkinter.Entry(win,bg="#2196F3",font=("Arial",8), textvariable=nombreUsuario).grid(row=0, column=1)

botonConectar = tkinter.Button(win, text="CONECTAR",font=("Arial Black",8), bg="#FFD600", command=iniciarHilos).grid(row=0, column=2)

textChat = tkinter.Text(win, height=5, width=40, bg="#00E5FF")
etiquetaChat= tkinter.Label(win, text="CHATS",font=("Arial Black",12)).grid(row=4, column=0)
textChat.grid(row=4, column=1)

listaConectados = Listbox(win,)
listaConectados.grid(row=4,column=2)

varEnviar = tkinter.Variable()
etiquetaEnviar = tkinter.Label(win, text="Escribir Mensaje:",font=("Arial",9)).grid(row=5, column=0)
entradaEnviar = tkinter.Entry(win, bg="#2196F3",textvariable=varEnviar).grid(row=5, column=1)

botonEnviarTodos = tkinter.Button(win, text="ENVIAR A TODOS", font=("Arial Black",8),bg="#304FFE", command=escribe_mensaje).grid(row=5, column=2)
botonEnviar = tkinter.Button(win, text="ENVIAR A", font=("Arial Black",8),bg="#FFD600", command=escribeMensajeUsuario).grid(row=6, column=2)
win.mainloop()


