import random


async def daily_message(level:int, amount:int) -> str:
        if(level == 0):
            return f"Daily claimed! {amount} credits added to balance."
        elif(level == 1):
            responses = [
                 f"You got a bonus! {amount} credits added to balance.",
                 f"What a start to the day! {amount} credits added to balance.",
                 f"I got something extra for you today. {amount} credits added to balance.",
            ]
            return random.choice(responses)
        else:
             responses = [
                  f"Fuck it. Here is a week worth of dailies.\n {amount} credits added to balance.",
                  f"I won big in Vegas! Here is a bit of my winnings.\n {amount} credits added to balance.",
             ]
             return random.choice(responses)