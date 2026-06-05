"""Card drawing utilities for Blackjack.

Cards are numbered 1–13: Ace=1, 2–10=face value, Jack=11, Queen=12, King=13.
Jack, Queen, and King are each worth 10 points.
"""

from random import randint

CARD_NAMES = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}


def draw_card() -> int:
    """Return a random card value between 1 and 13."""
    return randint(1, 13)


def card_name(card: int) -> str:
    """Return the display name for a card number."""
    return CARD_NAMES.get(card, str(card))


def card_points(card: int) -> int:
    """Return the blackjack point value (Jack/Queen/King count as 10)."""
    if card in (11, 12, 13):
        return 10
    return card
