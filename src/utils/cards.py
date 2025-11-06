
import requests

class Cards:
    
    values = {
        "ACE": "Туз", "KING": "Король", "QUEEN": "Дама", "JACK": "Валет",
        "10": "10", "9": "9", "8": "8", "7": "7", "6": "6",
        "5": "5", "4": "4", "3": "3", "2": "2"
    }

    suits = {
        "SPADES": "пики",
        "HEARTS": "червы",
        "DIAMONDS": "бубны",
        "CLUBS": "креста"
    }

    def get_cards(self, count: int = 1):
        url = f"https://deckofcardsapi.com/api/deck/new/draw/?count={count}"
        response = requests.get(url).json()
        cards = response["cards"]

        result = []
        for card in cards:
            value = self.values.get(card["value"], card["value"])
            suit = self.suits.get(card["suit"], card["suit"])
            result.append(f"{value} {suit}")
        return result
