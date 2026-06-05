"""Card drawing utilities for Blackjack.

Cards are numbered 1–13: Ace=1, 2–10=face value, Jack=11, Queen=12, King=13.
Each card's point value equals its number (Jack=11pts, Queen=12pts, King=13pts).
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
    """Return the point value for a card (equals its number: Jack=11, Queen=12, King=13)."""
    return card
