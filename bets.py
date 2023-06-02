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

#fix bet class (its shit rn)

class Bet():
    def __init__(self, title:str, id:int):
        self.title = title
        self.id = id
        self.outcomes = list()

    def add_outcome(self, title):
        new = Outcome(title)
        self.outcomes.append(new)


    def add_user_to_outcome(self, index, user, amt):
        self.outcomes[index].fix_amount(user, amt)


    def bet_on_outcome(self, name, user, amount):
        for outcome in self.outcomes:
            if outcome.name == name:
                if user not in outcome.users:
                    outcome.users.append(user)
                    outcome.bets[user] = 0
                outcome.total_amount += amount
                outcome.bets[user] += amount

    def get_subscribers(self, outcome_name):
        for outcome in self.outcomes:
            if outcome.name == outcome_name:
                return outcome

class Outcome():
    def __init__(self, title:str):
        self.users = dict()
        self.title = title
        self.total_amount = 0
  
    def fix_amount(self, user:str, amt:int):
        if(user in self.users.keys()):
            self.total_amount -= self.users[user]
        self.users[user] = amt
        self.total_amount += amt

        

