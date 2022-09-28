from cgitb import text
from distutils.command.config import config
import socket
import stat   
import threading
import tkinter
from tkinter import *

#Canal de comunicacion por Socket TCP
host = '172.31.0.224'
puerto =55555
estado = 0


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recibe_mensaje():
    #se solicita la conexión
    cliente.connect((host, puerto))
   
    while True:
        try:
            #se reciben mensajes
            mensaje = cliente.recv(1024).decode('utf-8')
            
            #la primera vez , se va a enviar el nombre de usuario
            if mensaje == "@nombreUsuario":
                cliente.send(nombreUsuario.get().encode("utf-8"))
            #se muestra la lista de usuarios conectados
            elif (mensaje[:8] == "ChatBot:"):
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
        mensaje = f"{nombreUsuario.get()}: {varEnviar.get()}"
        cliente.send(mensaje.encode('utf-8'))

def escribeMensajeUsuario():
    if(listaConectados.get(ANCHOR)!=""):
     print ("destino=",listaConectados.get(ANCHOR),sep="")
     data = f"{listaConectados.get(ANCHOR)}"
     cliente.send(data.encode("utf-8"))
     escribe_mensaje()

#cuando se toca el botón de conectar, se realiza la conexión con el socket
def iniciarHilos():
    global estado 
    #verifica que no se haya conectado antes
    #El campo de nombre no puede ser vacio
    if (nombreUsuario.get()!="" and estado == 0):
        estado=1
        recibe_hilo = threading.Thread(target=recibe_mensaje)
        recibe_hilo.start()


#ventana del cliente 
win = tkinter.Tk()  
win.title('Cliente TCP')
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





