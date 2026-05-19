from random import shuffle


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"'{self.rank} of {self.suit}'"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                if rank in ['Jack', 'Queen', 'King']:
                    self.cards.append(Card(suit, rank, 10))
                elif rank in ['Ace']:
                    self.cards.append(Card(suit, rank, 11))
                else:
                    self.cards.append(Card(suit, rank, int(rank)))

        shuffle(self.cards)
