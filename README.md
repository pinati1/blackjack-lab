# Blackjack CLI

Ori Cohen, ID 211481791

Exercise 1 - CLI Blackjack game written in Python.

## How to run

```
python main.py
```


## How it works

The game prints the welcome art, then deals you a card. You're asked if you want
another one (`y`/`n`). Keep hitting until you stop or go over 21. An Ace counts as
11 unless that would bust you, in which case it drops to 1 automatically.



## Test scenarios

**1. Player busts**

```
Your card: 8
Do you want another card? (y/n): y
Your cards: 8, 8
Your sum: 16
Do you want another card? (y/n): y
Your cards: 8, 8, 4
Your sum: 20
Do you want another card? (y/n): y
Your cards: 8, 8, 4, 2
Your sum: 22
You Lost
```
Player goes over 21, game ends immediately with "You Lost".

**2. Player wins (CPU busts), invalid input handled along the way**

```
Your card: 8
Do you want another card? (y/n): maybe
Invalid input. Please enter 'y' for yes or 'n' for no.
Do you want another card? (y/n): y
Your cards: 8, 8
Your sum: 16
Do you want another card? (y/n): n
CPU draws: 9 | CPU sum: 9
CPU draws: 5 | CPU sum: 14
CPU draws: 13 | CPU sum: 27
You Won
```
Typing something other than `y`/`n` just re-prompts instead of crashing.
CPU keeps drawing past 21 trying to beat 16, busts, player wins.

**3. CPU wins**

```
Your card: 13
Do you want another card? (y/n): n
CPU draws: 4 | CPU sum: 4
CPU draws: 2 | CPU sum: 6
CPU draws: 8 | CPU sum: 14
CPU won
```
Player stops at 13, CPU draws up past that without busting, CPU wins.

See `demo.txt` for the raw terminal output of these same runs.
