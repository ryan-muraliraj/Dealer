from random import randint
from typing import TypeVar
BetType = TypeVar("BetType", bound="Bet")

class BetManager():

    def __init__(self) -> None:
        self.bets = dict()
    
    def create_bet(self, title:str) -> int:
        is_valid_id = False
        new_id = 0
        while(not(is_valid_id)):
            new_id = randint(10000000,99999999)
            if(not(self.exists(new_id))):
                is_valid_id = True
            else:
                pass
        self.bets[new_id] = Bet(title, new_id)
        return new_id
    
    def exists(self, id:int) -> bool:
        return id in self.bets.keys()
    
    def get_bet(self, id:int) -> BetType:
        if(self.exists(id)):
            return self.bets[id]
        else:
            return None
        
    def delete_bet(self, id:int) -> bool:
        if(self.exists(id)):
            del self.bets[id]
            return True
        else:
            return False



class Bet():

    def __init__(self, title:str, id:int) -> None:
        self.title = title
        self.id = id
        pass
        
