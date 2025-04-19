from players.player import Player
from typing import List
import random

class RandomPlayer(Player):
    def __init__(self, player_index: int):
        self.player_index = player_index
        self.remaining_cards = set(range(1, 16))

    def play(self, score_card: int, player_history: List[List[int]]) -> int:
        ret = random.choice(list(self.remaining_cards))
        self.remaining_cards.remove(ret)
        return ret
