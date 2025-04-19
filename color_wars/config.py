from players.random import RandomPlayer
from players.stupid import StupidPlayer

# List of players in the game, of form (player_name, player_class)
player_classes = [("Random Player #1", RandomPlayer), ("Random Player #2", RandomPlayer), ("Random Player #3", RandomPlayer), ("Stupid Player #1", StupidPlayer)] 

# Size of grid
grid_size = 64

# Number of games to run
num_games = 1
