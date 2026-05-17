from sre_parse import State

from assets.blackjack_art import logo
from player import Player,Dealer
from deck import Deck


class BlackjackGame:
    def __init__(self):
        print(logo)
        print("Welcome to Blackjack!")
        self.deck = Deck()
        self.player = Player("player1")
        self.dealer = Dealer()
        self.state = State()
        self.round = 0


    def draw_card(self):
        return self.deck.cards.pop(0)


    def hit(self,player):

        new_card = self.draw_card()
        if new_card.suit is 'Ace':
            if self.player.sum+11>21:
                self.player.sum+=1
            else:
                self.player.sum += new_card.value
        self.player.hand.append(new_card)



    def deal_cards(self):
        for i in range(2):
            self.hit(self.player)
            self.hit(self.dealer)

    def start(self):
        self.deal_cards()
        #check if won
        print(f"your cards: {self.player.hand}")
        print(f"your sum: {self.player.sum}")
        print(f"dealer cards: {self.dealer.hand[0]}")
        choice = input("do you want another card? (y/n)")
        while choice is 'y':
            self.hit(self.player)
            print(f"your cards: {self.player.hand}")
            print(f"your sum: {self.player.sum}")
            choice = input("do you want another card? (y/n)")
        while self.dealer.sum<17:
            self.hit(self.dealer)

        pass
