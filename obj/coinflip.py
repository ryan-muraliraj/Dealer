import random
from typing import TypeVar
CoinObj = TypeVar("CoinObj", bound="CoinFlip")

class CoinFlipManager():
    def __init__(self):
        self.coinflips = dict()
    
    def create_cf(self, opt = None) -> int:
        is_valid_id = False
        new_id = 0
        while(not(is_valid_id)):
            new_id = random.randint(10000000,99999999)
            if(not(self.exists(new_id))):
                is_valid_id = True
            else:
                pass
        self.coinflips[new_id] = CoinFlip(new_id, opt)
        return new_id

    def exists(self, id:int) -> bool:
        return id in self.coinflips.keys()
    
    def get_cf(self, id:int) -> CoinObj:
        if(self.exists(id)):
            return self.coinflips[id]
        else:
            return None        
        
    def delete_cf(self, id:int) -> bool:
        if(self.exists(id)):
            del self.coinflips[id]
            return True
        else:
            return False    

class CoinFlip():
    def __init__(self, id:int, optional_player:tuple = None):
        self.players = {"Heads" : None, "Tails" : None}
        self.id = id
        if(optional_player == None):
            pass
        else:
            self.players[optional_player[0]] = optional_player[1]

        
    def add_player(self, player:tuple): 
        if(self.players[player[0]] == None):
            self.players[player[0]] = player[1]
        else:
            pass
    
    def heads_taken(self):
        return self.players["Heads"] != None

    def tails_taken(self):
        return self.players["Tails"] != None
    

    def is_full(self) -> bool:
        return (self.heads_taken() and self.tails_taken())
    
    def is_in(self, player_name:str):
        return player_name in self.players.values()

        
    def compute(self) -> tuple:
        if(self.is_full()):
            rand = random.choices(list(self.players.keys()), k=1)
            return (rand[0], self.players[rand[0]])
        else:
            raise RuntimeError
        