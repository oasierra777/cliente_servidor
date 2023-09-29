class Player:
    
    def __init__(self):
        #name del player
        self._nick = ""
        #address client
        self._addr = ""
        #jugada piedra/papel/tijera
        self._gamble = ""
        self._points = 0
        self._port_callback = 0
        
    @property
    def nick(self):
        return self._nick
    
    @property
    def addr(self):
        return self._addr
    
    @property
    def gamble(self):
        return self._gamble
    
    @property
    def points(self):
        return self._points
    
    @property
    def port_callback(self):
        return self._port_callback
    
    @property
    def vacant(self):
        if self._nick == "":
            return True
        else:
            return False
        
    @property
    def not_gamble(self):
        if self._gamble == "":
            return True
        else:
            return False
        
    @nick.setter
    def nick(self, name):
        self._nick = name
        
    @addr.setter
    def addr(self, name):
        self._addr = name
        
    @gamble.setter
    def gamble(self, name):
        if name in ["piedra", "papel", "tijera"]:
            self._gamble = name
            
    @points.setter
    def points(self, name):
        self._points = name
        
    @port_callback.setter
    def port_callback(self, port):
        self._port_callback = int(port)
        
    def rate(self):
        print(self._points)
        self._points += 1
        
    def settle(self, another_player):
        #retorna 0 si hay empate, -1 si gana el otro Player, 1si gana el objeto actual
        if((self.gamble == "piedra" and another_player.gamble == "tijera") or
            (self.gamble == "tijera" and another_player.gamble == "papel") or
            (self.gamble == "papel" and another_player.gamble == "piedra")):
            return 1
        elif ((self.gamble == "piedra" and another_player.gamble == "tijera") or
            (self.gamble == "tijera" and another_player.gamble == "papel") or
            (self.gamble == "papel" and another_player.gamble == "piedra")):
            return -1
        else:
            return 0
