"""Core game logic for the Blackjack CLI."""

from assets.blackjack_art import logo
from src.player import Player, CPU
from src.deck import draw_card, card_name, card_points


def add_card_to_hand(player: Player, card: int) -> None:
    """Add a card to a player's hand and update their sum.

    Ace is counted as 11 if it doesn't cause a bust; otherwise as 1.
    If an Ace previously counted as 11 causes the sum to exceed 21,
    it is automatically converted to 1.
    """
    player.hand.append(card)

    if card == 1:  # Ace
        if player.sum + 11 <= 21:
            player.sum += 11
            player.aces_as_eleven += 1
        else:
            player.sum += 1
    else:
        player.sum += card_points(card)

    # Convert an Ace from 11 → 1 if sum exceeds 21
    while player.sum > 21 and player.aces_as_eleven > 0:
        player.sum -= 10
        player.aces_as_eleven -= 1


def hand_display(hand: list[int]) -> str:
    """Return a comma-separated string of card names in the hand."""
    return ", ".join(card_name(c) for c in hand)


def player_turn(player: Player) -> bool:
    """Run the user's turn.

    Returns True if the player busts (sum > 21), False otherwise.
    """
    first_card = draw_card()
    add_card_to_hand(player, first_card)
    print(f"Your card: {card_name(first_card)}")

    while True:
        choice = input("Do you want another card? (yes/no): ").strip().lower()
        if choice not in ("yes", "no"):
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

        if choice == "no":
            break

        card = draw_card()
        add_card_to_hand(player, card)
        print(f"Your cards: {hand_display(player.hand)}")
        print(f"Your sum: {player.sum}")

        if player.sum > 21:
            print("You Lost")
            return True

    return False


def cpu_turn(cpu: CPU, user_sum: int) -> None:
    """Run the CPU's turn against the player's final sum.

    CPU draws cards until its sum is at least the user's sum,
    then the winner is determined.
    """
    while cpu.sum < user_sum:
        card = draw_card()
        add_card_to_hand(cpu, card)
        print(f"CPU draws: {card_name(card)} | CPU sum: {cpu.sum}")

        if cpu.sum > 21:
            print("You Won")
            return

    if cpu.sum == 21 and user_sum == 21:
        print("It's a tie")
    elif cpu.sum > user_sum:
        print("CPU won")
    else:
        # cpu.sum == user_sum but not both 21 → CPU failed to beat the player
        print("You Won")


def run_game() -> None:
    """Start and run a full game of Blackjack."""
    print(logo)

    player = Player("Player")
    cpu = CPU()

    if player_turn(player):
        return

    cpu_turn(cpu, player.sum)
