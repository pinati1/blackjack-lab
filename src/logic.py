from sre_parse import State

from assets.blackjack_art import logo
from src.player import Player, Dealer
from src.deck import Deck
from src.state import State

class BlackjackGame:
    def __init__(self):
        print(logo)
        print("Welcome to Blackjack!")
        self.deck = Deck()
        self.player = Player("player1")
        self.dealer = Dealer()
        self.state = State(self.player, self.dealer)

    def draw_card(self):
        return self.deck.cards.pop(0)

    def hit(self, player):

        new_card = self.draw_card()
        if new_card.rank == 'Ace':
            if player.sum + 11 > 21:
                player.sum += 1
            else:
                player.sum += new_card.value
        player.hand.append(new_card)

    def deal_cards(self):
        for i in range(2):
            self.hit(self.player)
            self.hit(self.dealer)

    def start(self):
        self.deal_cards()
        print(f"your cards: {self.player.hand}")
        print(f"your sum: {self.player.sum}")
        print(f"dealer cards: {self.dealer.hand[0]}")
        if self.state.check_state():
            print(f"{self.state.state}")
            return
        choice = input("do you want another card? (y/n)")
        while choice == 'y':
            self.hit(self.player)
            print(f"your cards: {self.player.hand}")
            print(f"your sum: {self.player.sum}")
            if self.state.check_state():
                print(f"{self.state.state}")
                return
            choice = input("do you want another card? (y/n)")
        while self.dealer.sum < 17:
            self.hit(self.dealer)
            if self.state.check_state():
                print(f"{self.state.state}")
                return
        print(f"{self.state.state}")


