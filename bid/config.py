from players.random import RandomPlayer
from players.greedy import GreedyPlayer

# List of players in the game, of form (player_name, player_class)
player_classes = [("Random Player #1", RandomPlayer), ("Random Player #2", RandomPlayer), ("Random Player #3", RandomPlayer), ("Greedy Player #1", GreedyPlayer)] 

# Number of games to run
num_games = 100 
