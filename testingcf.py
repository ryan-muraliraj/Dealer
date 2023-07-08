from coinflip import CoinFlipManager, CoinFlip

CFM = CoinFlipManager()

cf1 = CFM.create_cf()
print(f"Coinflip object created with ID: {cf1}")

cf1obj = CFM.get_cf(cf1)
print(cf1obj)
print(f"Retrieving the ID directly from the object: {cf1obj.id}")

def check_if_full(cf : CoinFlip):
    print(f"The coinflip (#{cf.id}) has both players registered. Ready to flip." if cf.is_full() else f"The coinflip (#{cf.id}) does not have both players registered.")


check_if_full(cf1obj)
cf1obj.add_player(("Heads", "krummy"))

check_if_full(cf1obj)
cf1obj.add_player(("Tails", "hades"))
check_if_full(cf1obj)
print(cf1obj.players.keys())

print(cf1obj.compute())





