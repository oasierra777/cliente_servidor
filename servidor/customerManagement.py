import socket
import threading

from player import Player

class CustomerManagement(threading.Thread):
    
    def __init__(self, client_address, client_socket, player1, player2, lock):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        self.c_address = client_address
        self.port_listen_cli = 0
        self.player1 = player1
        self.player2 = player2
        self.lock = lock
        
    def run(self):
        global num_gamble_current
        print("Escuchamos las peticiones del cliente: ", self.c_address)
        #mensaje de bienvenida con el protocolo
        welcome = "INSCRIBIR#nombre#puerto_escucha#\nJUGADA#{piedra|papel|tijera}#\n#PUNTUACIÓN"
        self.c_socket.send(bytes(welcome, 'UTF-8'))
        
        while True:
            data = self.c_socket.recv(512).decode('utf-8')
            print("Enviado desde cliente: <",data,">")
            subdata = data.split("#")
            respond = "#OK"
            
            if subdata[1] == "INSCRIBIR":
                if self.player1.vacant:
                    self.player1.nick = subdata[2]
                    self.player1.addr = self.c_address
                    self.player1.port_callback = subdata[3]
                elif self.player2.vacant:
                        self.player2.nick = subdata[2]
                        self.player2.addr = self.c_address
                        self.player2.port_callback = subdata[3]
                else:
                    respond = "#NOK#ya hay jugando dos personas#"
            elif subdata[1] == "JUGADA":
                #comprobamos el valor
                if subdata[2] not in ["piedra", "papel", "tijera"]:
                    respond = "#NOK#valores válidos: piedra|papel|tijera"
                #comprobamos la autenticidad SOCKET registrados
                elif self.c_address in [self.player1.addr, self.player2.addr]:
                    #estamos con el jugador 1
                    if self.c_address == self.player1.addr:
                        self.player1.gamble = subdata[2]
                    #estamos con el jugador 2
                    else:
                        self.player2.gamble = subdata[2]
                    respond = "#OK"
                    #se comprueba si se puede arbitrar la gamble
                    with self.lock:
                        if (not self.player1.not_gamble and not self.player2.not_gamble):
                            #gana el 1
                            if self.player1.settle(self.player2) > 0:
                                self.player1.rate()
                                result = "#OK#GANADOR:"+self.player1.nick+"#"
                            #gana el 2
                            elif self.player1.settle(self.player2) < 0:
                                self.player2.rate()
                                result = "#OK#GANADOR:"+self.player2.nick+"#"
                            else:
                                result = "OK#EMPATE"
                            self.player1.gamble = ""
                            self.player2.gamble = ""
                            
                            t1 = threading.Thread(target=self.comunicate_client_result, args=(result, 1))
                            t2 = threading.Thread(target=self.comunicate_client_result, args=(result, 2))
                            
                            t1.start()
                            t2.start()
                        
                #SOCKET no esta en la partida
                else:
                    respond = "#NOK#el jugador no esta en la partida"
            
            elif subdata[1] == 'PUNTUACION':
                respond = "#NOK#"+self.player1.nick+":"+str(self.player1.points)+"#"+self.player2.nick+":"+str(self.player2.points)+"#"
            
            self.c_socket.send(bytes(respond, 'UTF-8'))
        
    def comunicate_client_result(self, result, player_number):
        
        if player_number == 1:
            port = self.player1.port_callback
        elif player_number == 2:
            port = self.player2.port_callback
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((self.c_address[0], port))
            cli.sendall(bytes(result, 'UTF-8'))
            print("result enviado a"+self.c_address[0]+":"+cli.recv(1024).decode())
