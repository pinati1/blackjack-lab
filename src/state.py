from player import Player
class State:
    def __init__(self,player,dealer):
        self.player = player
        self.dealer = dealer
        

    def is_tie(self):
        if self.player.sum == 21 and self.dealer.sum == 21:
            return True
        return False


    def is_win(self):
        if self.player.sum > 21 and not self.is_tie():
            return True
        return False


    def is_busted(self):
        if self.player.sum > 21:
            self.player.is_busted = True
        if self.dealer.sum > 21:
            self.dealer.is_busted = True