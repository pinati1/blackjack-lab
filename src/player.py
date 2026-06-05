"""Player classes for Blackjack."""


class Player:
    """Represents a human player with a hand and running sum."""

    def __init__(self, name: str):
        self.name = name
        self.hand: list[int] = []
        self.sum: int = 0
        self.aces_as_eleven: int = 0  # tracks Aces currently counted as 11


class CPU(Player):
    """Represents the CPU opponent."""

    def __init__(self):
        super().__init__("CPU")
