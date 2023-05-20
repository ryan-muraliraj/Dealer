from bets import BetManager, Bet

BM = BetManager()

bet1id = BM.create_bet("WILL RYAN WIN HIS COMP GAME?")
bet2id = BM.create_bet("WILL RYAN GO POSITIVE THIS GAME?!")
bet3id = 12345678

bet1 = BM.get_bet(bet1id)
bet2 = BM.get_bet(bet2id)
bet3 = BM.get_bet(bet3id)

print(f"Bet 1: '{bet1.title}' exists" if BM.exists(bet1id) else "Bet 1: does not exist")
print(f"Bet 2: '{bet2.title}' exists" if BM.exists(bet2id) else "Bet 2: does not exist")
print(f"Bet 3: '{bet3.title}' exists" if BM.exists(bet3id) else "Bet 3: does not exist") 