from typing import List, Tuple
from players.player import Player
import random

class RandomPlayer(Player):
    def __init__(self, player_index: int, grid_size: int, num_players: int):
        self.player_index = player_index
        self.grid_size = grid_size
        self.num_players = num_players

    def play(self, board: List[List[int]], history: List[List[Tuple[int, int]]]) -> Tuple[int, int]:
        c = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if board[x][y] == 0:
                    c.append((x, y))
        return random.choice(c)
