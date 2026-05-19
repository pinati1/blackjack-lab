import player


class State:
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.state = ""
        self.who_won = ""

    def is_tie(self) -> bool:
        return self.player.sum == 21 and self.dealer.sum == 21

    def is_player_won(self) -> bool:
        return self.player.sum == 21 and not self.dealer.sum == 21

    def is_dealer_won(self) -> bool:
        return self.dealer.sum == 21 and not self.player.sum == 21

    def is_busted(self, player):
        if player.sum > 21:
            player.is_busted = True
            self.state = f"{player.__class__.__name__} busted"
            if player.__class__.__name__ == "Dealer":
                self.who_won = self.player
            else:
                self.who_won = self.dealer


    def check_win(self):
        if self.is_player_won():
            self.state = "player won"
            return
        if self.is_dealer_won():
            self.state = "dealer won"

    def is_end_game(self) -> bool:
        return self.state != ""

    def end_game(self):
        if self.player.sum > self.dealer.sum:
            self.state = "player won"
        else:
            self.state = "dealer won"

    def check_state(self) -> bool:
        self.is_busted(self.player)
        self.is_busted(self.dealer)
        if self.is_end_game():
            return True
        self.check_win()
        if self.is_end_game():
            return True
        self.is_tie()
        if self.is_end_game():
            return True
        return self.is_end_game()
