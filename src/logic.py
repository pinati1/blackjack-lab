from src.blackjack_art import logo
from src.player import Player, CPU
from src.deck import draw_card, card_points


def add_card_to_hand(player: Player, card: int) -> None:
    player.hand.append(card)

    if card == 1:
        if player.sum + 11 <= 21:
            player.sum += 11
            player.aces_as_eleven += 1
        else:
            player.sum += 1
    else:
        player.sum += card_points(card)

    while player.sum > 21 and player.aces_as_eleven > 0:
        player.sum -= 10
        player.aces_as_eleven -= 1


def card_label(card: int) -> str:
    return "Ace" if card == 1 else str(card)


def hand_display(hand: list[int]) -> str:
    return ", ".join(card_label(c) for c in hand)


def player_turn(player: Player) -> bool:
    first_card = draw_card()
    add_card_to_hand(player, first_card)
    print(f"Your card: {card_label(first_card)}")

    while True:
        choice = input("Do you want another card? (y/n): ").strip().lower()
        if choice not in ("y", "n"):
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            continue

        if choice == "n":
            break

        card = draw_card()
        add_card_to_hand(player, card)
        print(f"Your cards: {hand_display(player.hand)}")
        print(f"Your sum: {player.sum}")

        if player.sum > 21:
            print("You Lost")
            return True

        if player.sum == 21:
            print("You have 21!")
            break

    return False


def cpu_turn(cpu: CPU, user_sum: int) -> None:
    while cpu.sum < user_sum:
        card = draw_card()
        add_card_to_hand(cpu, card)
        print(f"CPU draws: {card_label(card)} | CPU sum: {cpu.sum}")

        if cpu.sum > 21:
            print("You Won")
            return

    if cpu.sum == user_sum:
        print("It's a tie")
    elif cpu.sum > user_sum:
        print("You Lose")
    else:
        print("You Won")


def run_game() -> None:
    print(logo)

    player = Player("Player")
    cpu = CPU()

    if player_turn(player):
        return

    if player.sum == 21 and len(player.hand) == 2:
        print("You Won")
        return

    cpu_turn(cpu, player.sum)
