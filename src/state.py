

class State:
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.state = ""

    def is_tie(self) -> bool:
        return self.player.sum == 21 and self.dealer.sum == 21

    def is_player_won(self) -> bool:
        return self.player.sum == 21 and not self.dealer.sum == 21

    def is_dealer_won(self) -> bool:
        return self.dealer.sum == 21 and not self.player.sum == 21

    def is_busted(self, player):
        if player.sum > 21:
            self.state = "busted"

    def check_win(self):
        if self.is_player_won():
            self.state = "player won"
            return
        if self.is_dealer_won():
            self.state = "dealer won"

    def is_end_game(self) -> bool:
        return self.state is not None

    def check_state(self) -> bool:

        self.check_win()
        if self.is_end_game():
            return True
        self.is_tie()
        return self.is_end_game()
