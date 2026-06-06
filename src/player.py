class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[int] = []
        self.sum: int = 0
        self.aces_as_eleven: int = 0


class CPU(Player):
    def __init__(self):
        super().__init__("CPU")
