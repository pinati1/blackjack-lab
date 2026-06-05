from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(r"C:\Users\Administrator\Desktop\programinbg lab 2\blackjack-lab")
SRC_ROOT = PROJECT_ROOT / "src"

for path in (str(PROJECT_ROOT), str(SRC_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from src.deck import Card, Deck
from src.logic import BlackjackGame
from src.player import Dealer, Player
from src.state import State


class FixedDeck:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards.copy()


class DeckTests(unittest.TestCase):
    def test_deck_contains_52_cards(self) -> None:
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_contains_4_aces(self) -> None:
        deck = Deck()
        ace_count = sum(1 for card in deck.cards if card.rank == "Ace")
        self.assertEqual(ace_count, 4)

    def test_face_cards_are_worth_10(self) -> None:
        deck = Deck()
        face_cards = [card for card in deck.cards if card.rank in {"Jack", "Queen", "King"}]
        self.assertTrue(face_cards)
        self.assertTrue(all(card.value == 10 for card in face_cards))

    def test_number_cards_match_rank_value(self) -> None:
        deck = Deck()
        numbered_cards = [card for card in deck.cards if card.rank.isdigit()]
        self.assertTrue(all(card.value == int(card.rank) for card in numbered_cards))


class HitLogicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = BlackjackGame()

    def test_hit_adds_card_to_hand(self) -> None:
        self.game.deck = FixedDeck([Card("Hearts", "7", 7)])

        self.game.hit(self.game.player)

        self.assertEqual(len(self.game.player.hand), 1)
        self.assertEqual(self.game.player.hand[0].rank, "7")

    def test_hit_updates_sum_for_number_card(self) -> None:
        self.game.deck = FixedDeck([Card("Hearts", "8", 8)])

        self.game.hit(self.game.player)

        self.assertEqual(self.game.player.sum, 8)

    def test_hit_counts_ace_as_11_when_safe(self) -> None:
        self.game.deck = FixedDeck([Card("Spades", "Ace", 11)])

        self.game.hit(self.game.player)

        self.assertEqual(self.game.player.sum, 11)

    def test_hit_counts_ace_as_1_when_11_would_bust(self) -> None:
        self.game.player.sum = 15
        self.game.deck = FixedDeck([Card("Spades", "Ace", 11)])

        self.game.hit(self.game.player)

        self.assertEqual(self.game.player.sum, 16)

    def test_deal_cards_gives_two_cards_to_each_participant(self) -> None:
        self.game.deck = FixedDeck(
            [
                Card("Hearts", "5", 5),
                Card("Clubs", "6", 6),
                Card("Diamonds", "9", 9),
                Card("Spades", "10", 10),
            ]
        )

        self.game.deal_cards()

        self.assertEqual(len(self.game.player.hand), 2)
        self.assertEqual(len(self.game.dealer.hand), 2)
        self.assertEqual(self.game.player.sum, 14)
        self.assertEqual(self.game.dealer.sum, 16)

    def test_multiple_aces_should_rescore_to_prevent_bust(self) -> None:
        self.game.deck = FixedDeck(
            [
                Card("Spades", "Ace", 11),
                Card("Hearts", "Ace", 11),
                Card("Clubs", "9", 9),
            ]
        )

        self.game.hit(self.game.player)
        self.game.hit(self.game.player)
        self.game.hit(self.game.player)

        self.assertEqual(
            self.game.player.sum,
            21,
            "Two aces and a nine should total 21, not 31.",
        )


class StateTests(unittest.TestCase):
    def make_state(self, player_sum: int, dealer_sum: int) -> State:
        player = Player("player1")
        dealer = Dealer()
        player.sum = player_sum
        dealer.sum = dealer_sum
        return State(player, dealer)

    def test_player_blackjack_is_detected(self) -> None:
        state = self.make_state(21, 18)

        self.assertTrue(state.check_state())
        self.assertEqual(state.state, "player won")

    def test_dealer_blackjack_is_detected(self) -> None:
        state = self.make_state(18, 21)

        self.assertTrue(state.check_state())
        self.assertEqual(state.state, "dealer won")

    def test_player_bust_sets_winner_to_dealer(self) -> None:
        state = self.make_state(22, 17)

        self.assertTrue(state.check_state())
        self.assertEqual(state.state, "Player busted")
        self.assertEqual(state.who_won.__class__.__name__, "Dealer")

    def test_dealer_bust_sets_winner_to_player(self) -> None:
        state = self.make_state(20, 23)

        self.assertTrue(state.check_state())
        self.assertEqual(state.state, "Dealer busted")
        self.assertEqual(state.who_won.name, "player1")

    def test_blackjack_tie_should_end_game(self) -> None:
        state = self.make_state(21, 21)

        self.assertTrue(state.check_state(), "A double blackjack should end the game.")
        self.assertNotEqual(state.state, "", "A double blackjack should record a tie state.")

    def test_end_game_higher_player_score_wins(self) -> None:
        state = self.make_state(20, 19)
        state.end_game()

        self.assertEqual(state.state, "player won")

    def test_end_game_higher_dealer_score_wins(self) -> None:
        state = self.make_state(18, 19)
        state.end_game()

        self.assertEqual(state.state, "dealer won")

    def test_equal_scores_should_be_tie_at_end_game(self) -> None:
        state = self.make_state(19, 19)
        state.end_game()

        self.assertEqual(state.state.lower(), "tie", "Equal scores should not default to dealer.")


if __name__ == "__main__":
    unittest.main()
