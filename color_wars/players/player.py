from typing import List, Tuple
from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def __init__(self, player_index: int, grid_size: int, num_players: int):
        pass

    @abstractmethod
    def play(self, board: List[List[int]], history: List[List[Tuple[int, int]]]) -> Tuple[int, int]:
        pass
