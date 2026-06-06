from random import randint

CARD_NAMES = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}


def draw_card() -> int:
    return randint(1, 13)


def card_name(card: int) -> str:
    return CARD_NAMES.get(card, str(card))


def card_points(card: int) -> int:
    return card
