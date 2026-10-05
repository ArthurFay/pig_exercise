# Author: Cuong Le
# Date: 10/04/2026
# Course: Coding with AI
# A two-player Pig dice game where players roll to reach a chosen point total.

import random


class Die:
    """Represent a six-sided die that stores its most recent roll."""

    def __init__(self):
        """Initialize the die with no roll value."""
        self.value = None

    def roll(self):
        """
        Roll a six-sided die, store the result, and return it.
        
        >>> from unittest.mock import patch
        >>> die = Die()
        >>> with patch('random.randint', return_value=4):
        ...     die.roll()
        4
        >>> die.value
        4
        """
        self.value = random.randint(1, 6)
        return self.value

    def display(self):
        """
        Print an ASCII representation of a six-sided die with
        the current value.
            
        Doctest:
        >>> die = Die()
        >>> die.value = 1
        >>> die.display()
         ------- 
        |       |
        |   *   |
        |       |
         ------- 
        >>> die.value = 2
        >>> die.display()
         ------- 
        | *     |
        |       |
        |     * |
         ------- 
        """
        die = [
            " ------- ",
            "|       |",
            "|       |",
            "|       |",
            " ------- "
        ]
        if self.value == 1:
            die[2] = "|   *   |"
        elif self.value == 2:
            die[1] = "| *     |"
            die[3] = "|     * |"
        elif self.value == 3:
            die[1] = "| *     |"
            die[2] = "|   *   |"
            die[3] = "|     * |"
        elif self.value == 4:
            die[1] = "| *   * |"
            die[3] = "| *   * |"
        elif self.value == 5:
            die[1] = "| *   * |"
            die[2] = "|   *   |"
            die[3] = "| *   * |"
        elif self.value == 6:
            die[1] = "| * * * |"
            die[3] = "| * * * |"
        for line in die:
            print(line)


class PigGame:
    """Manage a two-player Pig dice game."""

    def __init__(self, player1="Player 1", player2="Player 2", winning_total=20):
        """Initialize a game with player names and a winning point total."""
        self.players = [player1, player2]
        self.scores = {player: 0 for player in self.players}
        self.winning_total = winning_total
        self.die = Die()

    def display_rules(self):
        """
        Display the rules of the Pig dice game.
        """
        print("~" * 50)
        print("Pig Dice Game Rules:")
        print(f"1. The game is played by two players: {self.players[0]} and {self.players[1]}.")
        print("2. Players take turns to roll a die as many times as they wish, adding the rolled value to a turn total.")
        print("3. If a player rolls a 1, they score nothing for that turn and it becomes the next player's turn.")
        print("4. A player can choose to hold (stop rolling) to add their turn total to their score.")
        print(f"5. The first player to reach or exceed {self.winning_total} points wins the game.")
        print("~" * 50)

    def print_scoreboard(self):
        """
        Print the current scores of both players.
        
        Doctest:
        >>> game = PigGame()
        >>> game.scores = {"Player 1": 10, "Player 2": 15}
        >>> game.print_scoreboard()
        <BLANKLINE>
        *****************
        *  SCOREBOARD   *
        *****************
        Player 1: 10
        Player 2: 15
        *****************
        <BLANKLINE>
        """
        print()
        print("*****************")
        print("*  SCOREBOARD   *")
        print("*****************")
        for player in self.players:
            print(f"{player}: {self.scores[player]}")
        print("*****************")
        print()

    def play_turn(self, player):
        """
        Play a single turn for the given player.

        Args:
            player (str): The name of the player taking this turn.

        Returns:
            int: The total points scored by the player in this turn.
        
        Doctest:
        >>> from unittest.mock import patch
        >>> with patch('builtins.input', side_effect=['y', 'y']):
        ...     with patch('random.randint', side_effect=[5, 6, 1]):
        ...         PigGame().play_turn("Player 1")
        PLAYER 1'S TURN
         ------- 
        | *   * |
        |   *   |
        | *   * |
         ------- 
        Total is 5
         ------- 
        | * * * |
        |       |
        | * * * |
         ------- 
        Total is 11
         ------- 
        |       |
        |   *   |
        |       |
         ------- 
        Player 1 rolled a 1! No points earned this turn.
        0
        >>> with patch('builtins.input', side_effect=['n']):
        ...     with patch('random.randint', side_effect=[4]):
        ...         PigGame().play_turn("Player 2")
        PLAYER 2'S TURN
         ------- 
        | *   * |
        |       |
        | *   * |
         ------- 
        Total is 4
        4
        """
        print(f"{player.upper()}'S TURN")
        turn_total = 0
        roll = self.die.roll()
        while roll != 1:
            self.die.display()
            turn_total += roll
            print(f"Total is {turn_total}")
            choice = input("Roll again? (y/n) ")
            if choice.lower() == 'n':
                return turn_total
            roll = self.die.roll()
        self.die.display()
        print(f"{player} rolled a 1! No points earned this turn.")
        return 0

    def play_game(self):
        """
        Play a game of Pig between the two players.
        Returns:
            bool: True if the game should be played again, 
            False otherwise.
        """
        self.scores = {player: 0 for player in self.players}
        while all(self.scores[player] < self.winning_total for player in self.players):
            for player in self.players:
                self.scores[player] += self.play_turn(player)
                self.print_scoreboard()
                if self.scores[player] >= self.winning_total:
                    print(f"{player} wins!")
                    again = input("Do you want to play again? (y/n) ").lower()
                    return again == 'y'
        return False


def main():
    """Collect game settings and run the Pig game."""
    # Use default player labels when either name is left blank.
    player1 = input("Enter Player 1 name: ").strip() or "Player 1"
    player2 = input("Enter Player 2 name: ").strip() or "Player 2"

    # Keep asking until the winning total is a positive whole number.
    while True:
        try:
            winning_total = int(input("Enter winning point total: "))
            if winning_total > 0:
                break
        except ValueError:
            pass
        print("Invalid input. Please enter a whole number greater than 0.")

    game = PigGame(player1, player2, winning_total)
    game.display_rules()
    print("\nLet's play Pig!\n")

    # Continue with another game whenever the players choose to replay.
    while game.play_game():
        pass
    print("Thanks for playing!")


if __name__ == "__main__":
    main()