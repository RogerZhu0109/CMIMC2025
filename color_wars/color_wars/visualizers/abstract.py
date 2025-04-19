from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path

class AbstractVisualizer(ABC):
    def __init__(self, N: int, P: int, filepath: Path):
        self._N = N
        self._P = P
        self._filepath = filepath
        pass

    @abstractmethod
    def add_break(self):
        pass

    @abstractmethod
    def save_frame(self, grid: List[List[int]], filepath: Optional[Path]=None) -> str:
        pass

    @abstractmethod
    def add_frame(self, grid: List[List[int]]):
        pass

    @abstractmethod
    def save_output(self, filepath: Optional[Path]=None) -> str:
        pass
