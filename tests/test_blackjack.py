"""Comprehensive pytest tests for the Blackjack CLI game (v2).

Covers every reachable game state:
  - card_points()       : face-card scoring
  - draw_card()         : range validation
  - add_card_to_hand()  : all Ace / bust / accumulation cases
  - hand_display()      : formatting
  - player_turn()       : stop, draw, bust, 21-auto-stop, invalid input, Ace flip
  - cpu_turn()          : CPU wins, CPU busts, tie, CPU matches non-21
  - run_game()          : full end-to-end smoke tests
"""

from __future__ import annotations

import pytest
from unittest.mock import patch

from src.player import Player, CPU
from src.deck import draw_card, card_points
from src.logic import add_card_to_hand, card_label, hand_display, player_turn, cpu_turn, run_game


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def player():
    return Player("TestPlayer")


@pytest.fixture
def cpu():
    return CPU()


# ─────────────────────────────────────────────
# card_points
# ─────────────────────────────────────────────

class TestCardPoints:
    """card_points() maps card numbers to blackjack scoring values."""

    @pytest.mark.parametrize("card", range(2, 11))
    def test_number_cards_return_face_value(self, card):
        assert card_points(card) == card

    def test_jack_worth_11(self):
        assert card_points(11) == 11

    def test_queen_worth_12(self):
        assert card_points(12) == 12

    def test_king_worth_13(self):
        assert card_points(13) == 13

    def test_ace_raw_value_is_1(self):
        # Ace special logic lives in add_card_to_hand; raw card_points = 1
        assert card_points(1) == 1


# ─────────────────────────────────────────────
# draw_card
# ─────────────────────────────────────────────

class TestDrawCard:
    """draw_card() must always return a value in [1, 13]."""

    def test_always_in_range(self):
        for _ in range(200):
            assert 1 <= draw_card() <= 13


# ─────────────────────────────────────────────
# add_card_to_hand
# ─────────────────────────────────────────────

class TestAddCardToHand:
    """All scoring and Ace-handling paths."""

    def test_card_appended_to_hand(self, player):
        add_card_to_hand(player, 7)
        assert player.hand == [7]

    def test_number_card_updates_sum(self, player):
        add_card_to_hand(player, 8)
        assert player.sum == 8

    def test_jack_worth_11(self, player):
        add_card_to_hand(player, 11)
        assert player.sum == 11

    def test_queen_worth_12(self, player):
        add_card_to_hand(player, 12)
        assert player.sum == 12

    def test_king_worth_13(self, player):
        add_card_to_hand(player, 13)
        assert player.sum == 13

    def test_multiple_face_cards_accumulate(self, player):
        add_card_to_hand(player, 5)
        add_card_to_hand(player, 7)
        assert player.sum == 12

    # ── Ace as 11 ──────────────────────────────

    def test_ace_counted_as_11_when_safe(self, player):
        add_card_to_hand(player, 1)
        assert player.sum == 11
        assert player.aces_as_eleven == 1

    def test_ace_and_ten_equals_21(self, player):
        add_card_to_hand(player, 1)   # Ace -> 11
        add_card_to_hand(player, 10)  # 11 + 10 = 21
        assert player.sum == 21
        assert player.aces_as_eleven == 1

    # ── Ace as 1 (drawn when already high) ─────

    def test_ace_counted_as_1_when_11_would_bust(self, player):
        player.sum = 15
        add_card_to_hand(player, 1)   # 15 + 11 = 26 > 21 -> count as 1
        assert player.sum == 16
        assert player.aces_as_eleven == 0

    # ── Ace auto-flip after subsequent card ─────

    def test_ace_flips_from_11_to_1_after_subsequent_card_busts(self, player):
        add_card_to_hand(player, 1)   # Ace -> 11
        add_card_to_hand(player, 9)   # 20
        add_card_to_hand(player, 5)   # 25 -> flip Ace -> 15
        assert player.sum == 15
        assert player.aces_as_eleven == 0

    def test_ace_flip_keeps_player_alive(self, player):
        add_card_to_hand(player, 1)   # Ace -> 11
        add_card_to_hand(player, 10)  # 21
        add_card_to_hand(player, 5)   # 26 -> flip Ace -> 16
        assert player.sum == 16
        assert player.aces_as_eleven == 0

    # ── Two Aces ────────────────────────────────

    def test_two_aces_first_11_second_1(self, player):
        add_card_to_hand(player, 1)   # Ace -> 11
        add_card_to_hand(player, 1)   # 11+11=22 > 21 -> second counts as 1 -> 12
        assert player.sum == 12
        assert player.aces_as_eleven == 1

    def test_two_aces_and_nine_equals_21(self, player):
        add_card_to_hand(player, 1)   # Ace -> 11
        add_card_to_hand(player, 1)   # 12
        add_card_to_hand(player, 9)   # 21
        assert player.sum == 21

    def test_three_aces_total_13(self, player):
        add_card_to_hand(player, 1)   # 11
        add_card_to_hand(player, 1)   # 12 (second counts as 1)
        add_card_to_hand(player, 1)   # 13 (third counts as 1)
        assert player.sum == 13

    # ── Multiple regular cards ───────────────────

    def test_multiple_cards_accumulate(self, player):
        for card in [5, 6, 7]:
            add_card_to_hand(player, card)
        assert player.sum == 18
        assert player.hand == [5, 6, 7]

    def test_sum_never_exceeds_21_with_ace_protection(self, player):
        add_card_to_hand(player, 1)
        add_card_to_hand(player, 9)
        add_card_to_hand(player, 5)   # would be 25 -> flip -> 15
        assert player.sum <= 21


# ─────────────────────────────────────────────
# card_label
# ─────────────────────────────────────────────

class TestCardLabel:
    """card_label() returns 'Ace' for card 1, raw number string otherwise."""

    def test_ace_returns_ace_string(self):
        assert card_label(1) == "Ace"

    def test_number_card_returns_string_of_number(self):
        assert card_label(7) == "7"

    def test_jack_displays_as_11(self):
        assert card_label(11) == "11"

    def test_queen_displays_as_12(self):
        assert card_label(12) == "12"

    def test_king_displays_as_13(self):
        assert card_label(13) == "13"


# ─────────────────────────────────────────────
# hand_display
# ─────────────────────────────────────────────

class TestHandDisplay:
    """hand_display() shows 'Ace' for card 1, raw numbers for everything else."""

    def test_empty_hand(self):
        assert hand_display([]) == ""

    def test_single_card(self):
        assert hand_display([7]) == "7"

    def test_multiple_cards(self):
        assert hand_display([7, 11, 3]) == "7, 11, 3"

    def test_face_cards_show_their_number(self):
        assert hand_display([11, 12, 13]) == "11, 12, 13"

    def test_ace_shows_as_ace_not_1(self):
        assert hand_display([1]) == "Ace"

    def test_ace_mixed_with_other_cards(self):
        assert hand_display([1, 9]) == "Ace, 9"


# ─────────────────────────────────────────────
# player_turn
# ─────────────────────────────────────────────

class TestPlayerTurn:
    """All branches inside player_turn()."""

    # ── Stops immediately ───────────────────────

    def test_player_stops_immediately_returns_false(self, player):
        with patch("src.logic.draw_card", return_value=7):
            with patch("builtins.input", return_value="n"):
                result = player_turn(player)
        assert result is False
        assert player.sum == 7

    def test_first_card_is_displayed(self, player, capsys):
        with patch("src.logic.draw_card", return_value=9):
            with patch("builtins.input", return_value="n"):
                player_turn(player)
        assert "Your card: 9" in capsys.readouterr().out

    # ── Draws extra cards then stops ────────────

    def test_player_draws_one_extra_card_then_stops(self, player, capsys):
        with patch("src.logic.draw_card", side_effect=[5, 9]):
            with patch("builtins.input", side_effect=["y", "n"]):
                result = player_turn(player)
        assert result is False
        assert player.sum == 14
        out = capsys.readouterr().out
        assert "Your cards: 5, 9" in out
        assert "Your sum: 14" in out

    def test_player_draws_multiple_cards_before_stopping(self, player):
        with patch("src.logic.draw_card", side_effect=[3, 4, 5, 2]):
            with patch("builtins.input", side_effect=["y", "y", "y", "n"]):
                result = player_turn(player)
        assert result is False
        assert player.sum == 14

    # ── Bust ────────────────────────────────────

    def test_player_busts_returns_true(self, player, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 8, 6]):
            with patch("builtins.input", side_effect=["y", "y"]):
                result = player_turn(player)
        assert result is True
        assert player.sum > 21
        assert "You Lost" in capsys.readouterr().out

    def test_bust_on_second_draw(self, player):
        with patch("src.logic.draw_card", side_effect=[10, 10, 5]):
            with patch("builtins.input", side_effect=["y", "y"]):
                result = player_turn(player)
        assert result is True

    # ── Hits exactly 21 ─────────────────────────

    def test_player_hits_21_returns_false(self, player):
        # 10 + 4 + 7 = 21
        with patch("src.logic.draw_card", side_effect=[10, 4, 7]):
            with patch("builtins.input", side_effect=["y", "y"]):
                result = player_turn(player)
        assert result is False
        assert player.sum == 21

    def test_player_hits_21_prints_message(self, player, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 4, 7]):
            with patch("builtins.input", side_effect=["y", "y"]):
                player_turn(player)
        assert "You have 21!" in capsys.readouterr().out

    def test_player_hits_21_no_further_prompt(self, player):
        # Only 2 "y" inputs; if a third input() were called it raises StopIteration
        with patch("src.logic.draw_card", side_effect=[10, 4, 7]):
            with patch("builtins.input", side_effect=["y", "y"]):
                player_turn(player)  # must not raise

    # ── Invalid input ────────────────────────────

    def test_invalid_input_re_prompts(self, player, capsys):
        with patch("src.logic.draw_card", return_value=8):
            with patch("builtins.input", side_effect=["maybe", "x", "n"]):
                player_turn(player)
        out = capsys.readouterr().out
        assert out.count("Invalid input") == 2

    def test_valid_input_after_invalid_accepted(self, player):
        with patch("src.logic.draw_card", return_value=6):
            with patch("builtins.input", side_effect=["oops", "n"]):
                result = player_turn(player)
        assert result is False

    # ── Ace handling ─────────────────────────────

    def test_ace_first_card_counted_as_11(self, player, capsys):
        with patch("src.logic.draw_card", return_value=1):
            with patch("builtins.input", return_value="n"):
                player_turn(player)
        assert player.sum == 11
        assert "Your card: Ace" in capsys.readouterr().out

    def test_ace_flips_to_prevent_bust_during_turn(self, player):
        # Ace(11) + 9 = 20, then 5 -> 25 -> flip -> 15
        with patch("src.logic.draw_card", side_effect=[1, 9, 5]):
            with patch("builtins.input", side_effect=["y", "y", "n"]):
                result = player_turn(player)
        assert result is False
        assert player.sum == 15


# ─────────────────────────────────────────────
# cpu_turn
# ─────────────────────────────────────────────

class TestCpuTurn:
    """All branches inside cpu_turn()."""

    # ── CPU wins ────────────────────────────────

    def test_cpu_wins_prints_you_lose(self, cpu, capsys):
        # user=15; cpu draws 10(10), 7(17) -> 17 > 15 -> You Lose
        with patch("src.logic.draw_card", side_effect=[10, 7]):
            cpu_turn(cpu, 15)
        assert "You Lose" in capsys.readouterr().out

    def test_cpu_wins_with_single_draw(self, cpu, capsys):
        with patch("src.logic.draw_card", return_value=9):
            cpu_turn(cpu, 5)
        assert "You Lose" in capsys.readouterr().out

    def test_cpu_draws_multiple_times_before_winning(self, cpu, capsys):
        # user=17; cpu: 5(5), 6(11), 7(18) -> You Lose
        with patch("src.logic.draw_card", side_effect=[5, 6, 7]):
            cpu_turn(cpu, 17)
        assert cpu.sum == 18
        assert "You Lose" in capsys.readouterr().out

    # ── CPU busts ───────────────────────────────

    def test_cpu_busts_prints_you_won(self, cpu, capsys):
        # user=20; cpu: 10(10), 8(18), 5(23>21) -> You Won
        with patch("src.logic.draw_card", side_effect=[10, 8, 5]):
            cpu_turn(cpu, 20)
        assert "You Won" in capsys.readouterr().out

    def test_cpu_busts_sum_exceeds_21(self, cpu, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 8, 5]):
            cpu_turn(cpu, 20)
        assert cpu.sum > 21

    # ── Tie ─────────────────────────────────────

    def test_tie_when_both_reach_21(self, cpu, capsys):
        # user=21; cpu draws 10 + Ace(11) = 21 -> tie
        with patch("src.logic.draw_card", side_effect=[10, 1]):
            cpu_turn(cpu, 21)
        assert "It's a tie" in capsys.readouterr().out

    def test_tie_cpu_sum_is_21(self, cpu, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 1]):
            cpu_turn(cpu, 21)
        assert cpu.sum == 21

    # ── CPU matches user → tie (any equal sum, real blackjack push rule) ──

    def test_cpu_matches_user_non_21_is_tie(self, cpu, capsys):
        # user=15; cpu draws 8(8), 7(15) -> equal -> tie
        with patch("src.logic.draw_card", side_effect=[8, 7]):
            cpu_turn(cpu, 15)
        assert "It's a tie" in capsys.readouterr().out

    def test_cpu_matches_user_at_21_is_tie(self, cpu, capsys):
        # user=21; cpu draws 10 + Ace(11) = 21 -> tie
        with patch("src.logic.draw_card", side_effect=[10, 1]):
            cpu_turn(cpu, 21)
        assert "It's a tie" in capsys.readouterr().out

    # ── Output format ────────────────────────────

    def test_cpu_draw_output_contains_card_value(self, cpu, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 7]):
            cpu_turn(cpu, 15)
        out = capsys.readouterr().out
        assert "CPU draws: 10" in out
        assert "CPU draws: 7" in out

    def test_cpu_draw_output_contains_updated_sum(self, cpu, capsys):
        with patch("src.logic.draw_card", side_effect=[10, 7]):
            cpu_turn(cpu, 15)
        out = capsys.readouterr().out
        assert "CPU sum: 10" in out
        assert "CPU sum: 17" in out

    # ── Ace handling for CPU ─────────────────────

    def test_cpu_ace_counted_as_11(self, cpu, capsys):
        # user=15; cpu draws 1(Ace=11), 5(16) -> 16 > 15 -> You Lose
        with patch("src.logic.draw_card", side_effect=[1, 5]):
            cpu_turn(cpu, 15)
        assert cpu.sum == 16
        out = capsys.readouterr().out
        assert "CPU draws: Ace" in out
        assert "You Lose" in out

    def test_cpu_ace_prevents_bust(self, cpu, capsys):
        # user=20; cpu draws 1(Ace=11, sum=11), 9(sum=20) -> equal -> tie
        with patch("src.logic.draw_card", side_effect=[1, 9]):
            cpu_turn(cpu, 20)
        assert cpu.sum == 20
        assert "It's a tie" in capsys.readouterr().out


# ─────────────────────────────────────────────
# run_game  (end-to-end smoke tests)
# ─────────────────────────────────────────────

class TestRunGame:
    """Full game smoke tests via run_game()."""

    def test_logo_is_printed(self, capsys):
        with patch("src.logic.draw_card", return_value=7):
            with patch("builtins.input", return_value="n"):
                run_game()
        out = capsys.readouterr().out
        # The logo contains the ASCII card art; check for its distinctive border
        assert ".------." in out

    def test_player_busts_ends_with_you_lost(self, capsys):
        # 10 + 8 + 6 = 24
        with patch("src.logic.draw_card", side_effect=[10, 8, 6]):
            with patch("builtins.input", side_effect=["y", "y"]):
                run_game()
        assert "You Lost" in capsys.readouterr().out

    def test_cpu_wins_ends_with_you_lose(self, capsys):
        # Player: first card=5, stops. CPU draws 9 -> 9 > 5 -> You Lose
        with patch("src.logic.draw_card", side_effect=[5, 9]):
            with patch("builtins.input", return_value="n"):
                run_game()
        assert "You Lose" in capsys.readouterr().out

    def test_tie_when_cpu_matches_player(self, capsys):
        # Player: 10, stops. CPU draws 10 -> equal sum -> tie
        with patch("src.logic.draw_card", side_effect=[10, 10]):
            with patch("builtins.input", return_value="n"):
                run_game()
        assert "It's a tie" in capsys.readouterr().out

    def test_player_hits_21_with_2_cards_wins_immediately(self, capsys):
        # Natural blackjack: first card(Ace=11) + one draw(10) = 21 -> CPU never plays
        with patch("src.logic.draw_card", side_effect=[1, 10]):
            with patch("builtins.input", side_effect=["y"]):
                run_game()
        out = capsys.readouterr().out
        assert "You have 21!" in out
        assert "You Won" in out
        assert "CPU draws" not in out

    def test_player_hits_21_with_3_plus_cards_cpu_plays(self, capsys):
        # 3-card 21: CPU still gets to play
        # Player: 5 + 9 + 7 = 21. CPU draws 10(10) -> 10 < 21, draws 13(10) -> 20 < 21,
        # draws 5 -> 25 bust -> You Won
        with patch("src.logic.draw_card", side_effect=[5, 9, 7, 10, 13, 5]):
            with patch("builtins.input", side_effect=["y", "y"]):
                run_game()
        out = capsys.readouterr().out
        assert "You have 21!" in out
        assert "CPU draws" in out  # CPU did play

    def test_player_hits_21_with_3_cards_cpu_ties(self, capsys):
        # 3-card 21: CPU reaches 21 too -> tie
        # Player: 5 + 9 + 7 = 21. CPU: 10 + Ace(11) = 21 -> tie
        with patch("src.logic.draw_card", side_effect=[5, 9, 7, 10, 1]):
            with patch("builtins.input", side_effect=["y", "y"]):
                run_game()
        out = capsys.readouterr().out
        assert "It's a tie" in out
