import random


class TournamentManager:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.games_played = 0
        self.wins = 0
        self.losses = 0

    def get_computer_choice(self):
        return random.choice(self.choices)

    def decide_winner(self, player_choice, computer_choice):
        self.games_played += 1
        if player_choice == computer_choice:
            return None
        if (player_choice == 'rock' and computer_choice == 'scissors') or \
           (player_choice == 'scissors' and computer_choice == 'paper') or \
           (player_choice == 'paper' and computer_choice == 'rock'):
            self.wins += 1
            return 'Player'
        else:
            self.losses += 1
            return 'Computer'

    def get_metrics(self):
        return self.games_played, self.wins, self.losses