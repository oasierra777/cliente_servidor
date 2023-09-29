import socket
import threading

from player import Player
from customerManagement import CustomerManagement

if __name__=='__main__':
    
    player1 = Player()
    player2 = Player()
    
    lock = threading.Lock()
    HOST = ""
    PORT = 2000
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print("Servidor iniciado. En espera del Cliente...")
    
    while True:
        server.listen(1)
        client_sock, client_address = server.accept()
        t = CustomerManagement(client_address, client_sock, player1, player2, lock)
        t.start()
