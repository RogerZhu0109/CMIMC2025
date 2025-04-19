from abc import ABC, abstractmethod
from typing import List

class Player(ABC):
    @abstractmethod
    def __init__(self, player_index: int):
        pass

    @abstractmethod
    def play(self, score_card: int, player_history: List[List[int]]) -> int:
        pass
