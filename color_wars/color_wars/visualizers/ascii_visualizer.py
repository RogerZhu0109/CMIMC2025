from visualizers.abstract import AbstractVisualizer
from typing import List, Optional
from pathlib import Path
import termcolor

class AsciiVisualizer(AbstractVisualizer):
    EMPTY_COL = "on_white"
    SHARED_COL = "on_grey"
    PLAYER_COLS = ["on_red", "on_blue", "on_yellow", "on_green"]
    default_extension = ".txt"

    def __init__(self, N: int, P: int, filepath: Optional[Path]=None, highlight_player=None):
        assert P <= 4
        if filepath is None:
            filepath = Path.cwd() / "image.txt"
        super().__init__(N, P, filepath)
        
        self._colormap = [AsciiVisualizer.SHARED_COL] * (2 ** P)
        self._colormap[0] = AsciiVisualizer.EMPTY_COL
        for i in range(P):
            self._colormap[2**i] = AsciiVisualizer.PLAYER_COLS[i]
        self._frames = []
        self._highlight_bit = 1 << highlight_player if highlight_player is not None else 0

    def _block(self, val: int) -> str:
        attrs = ["bold"] if val & self._highlight_bit else None
        return termcolor.colored("  ", on_color=self._colormap[val], attrs=attrs)

    def _frame(self, grid):
        return "\n".join(
            "".join(self._block(val) for val in row)
            for row in grid
        ) + "\n"

    @property
    def _legend(self) -> str:
        buf = self._block
        res  = f"{buf(0)}: Empty\n"
        res += f"{buf(3 if self._P >= 2 else 1)}: Shared\n"
        for i in range(self._P):
            label = "You" if (1 << i) == self._highlight_bit else f"Player {i}"
            res += f"{buf(1 << i)}: {label}\n"
        return res

    @property
    def _br(self) -> str:
        return "--" * self._N + "\n"

    def add_break(self) -> None:
        self._frames.append(self._br * 2)
    
    def save_frame(self, grid: List[List[int]], filepath: Optional[Path]=None) -> str:
        if filepath is None:
            filepath = self._filepath

        res = self._legend + self._br + self._frame(grid)
        with filepath.open("w", encoding="utf-8") as file:
            file.write(res)
        return f"Visualization saved to {filepath}"

    def add_frame(self, grid: List[List[int]]):
        self._frames.append(self._frame(grid))

    def save_output(self, filepath: Optional[Path]=None) -> str:
        if filepath is None:
            filepath = self._filepath
        res = self._legend + self._br + self._br.join(self._frames)
        with filepath.open("w", encoding="utf-8") as file:
            file.write(res)
        return f"Visualization saved to {filepath}"
