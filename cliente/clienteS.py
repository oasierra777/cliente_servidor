import socket
import threading
from tkinter import *

def conect_server(port_call_back):
    
    global client
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    lblInfo["text"] = client.recv(1024).decode()
    t = threading.Thread(target=listen_answer, args=(port_call_back,))
    t.daemon = True
    t.start()
    
def sing_up(port_cli):
    global client
    client.sendall(bytes("#INSCRIBIR#"+entName.get()+"#"+port_cli+"#", "UTF-8"))
    lblInfo["text"] = client.recv(1024).decode()
    
def send_play(gamble):
    global client
    client.sendall(bytes("#JUGADA#"+gamble+"#", "UTF-8"))
    lblInfo["text"] = client.recv(1024).decode()
    
def check_points():
    global client
    client.sendall(bytes("#PUNTUACION#", "UTF-8"))
    lblInfo["text"] = client.recv(1024).decode()
    
def listen_answer(port_call_back):
    
    global information
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER, port_call_back))
        print("Escucha en callback")
        s.listen()
        while True:
            (cli, add) = s.accept()
            with cli:
                data = cli.recv(512).decode("UTF-8")
                print("Enviado desde el cliente:<",data,">")
                information = data
                fPPT.event_generate("<<er>>", when="tail")
                cli.send(bytes("#OK#", "UFT-8"))
                
def write_resolution(*args):
    lblInfo["text"] = information
    
SERVER = "127.0.0.1"
PORT = 2000
cliente = None
information = ""
fPPT = Tk()
fPPT.title("Piedra-Papel-Tijera")
fPPT.geometry("300x300")
fPPT.resizable(True, True)
lblInfo = Label(fPPT, text=information)
lblInfo.place(x=0, y=230)
lblPort = Label(fPPT, text="Puerto de escucha: ")
lblPort.place(x=0, y=50)
entPort = Entry(fPPT,)
entPort.place(x=110, y=50, width=30)
btnConn = Button(fPPT, text="Conectar", command = lambda: conect_server(int(entPort.get())))
btnConn.place(x=150, y=50)
entName = Entry(fPPT,)
entName.place(x=20, y=100)
btnEnroll = Button(fPPT, text="Inscribir", command=lambda: sing_up(entPort.get()))
btnEnroll.place(x=150, y=100)
btnStone = Button(fPPT, text="Piedra", command= lambda:send_play("piedra"))
btnStone.place(x=50, y=150)
btnPaper = Button(fPPT, text="Papel", command= lambda:send_play("papel"))
btnPaper.place(x=100, y=150)
btnFork = Button(fPPT, text="Tijera", command= lambda:send_play("tijera"))
btnFork.place(x=150, y=150)
btnPoint = Button(fPPT, text="Puntuacion", command=check_points)
btnPoint.place(x=150, y=200)
fPPT.bind("<<er>>", write_resolution)
fPPT.mainloop()
