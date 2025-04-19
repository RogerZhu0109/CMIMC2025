from visualizers.abstract import AbstractVisualizer
from typing import List, Optional
from pathlib import Path
from PIL import Image, ImageDraw

class ImageVisualizer(AbstractVisualizer):
    EMPTY_COL = "white"
    SHARED_COL = "gray"
    PLAYER_COLS = ["red", "blue", "yellow", "green"]
    default_extension = ".gif"

    def __init__(self, N: int, P: int, filepath: Optional[Path]=None, cell_size: int=10, highlight_player=None):
        assert P <= 4
        if filepath is None:
            filepath = Path.cwd() / "image.jpg"
        super().__init__(N, P, filepath)
        self._cell_size = cell_size

        self._colormap = [ImageVisualizer.SHARED_COL] * (2 ** P)
        self._colormap[0] = ImageVisualizer.EMPTY_COL
        for i in range(P):
            self._colormap[2 ** i] = ImageVisualizer.PLAYER_COLS[i]

        self._frames = []
        self._highlight_bit = 1 << highlight_player if highlight_player is not None else 0

    def _frame(self, grid: List[List[int]]) -> Image.Image:
        num_rows = len(grid)
        num_cols = len(grid[0]) if num_rows > 0 else 0

        width = num_cols * self._cell_size
        height = num_rows * self._cell_size
        img = Image.new("RGB", (width, height), self._colormap[0])
        draw = ImageDraw.Draw(img)

        for row_idx, row in enumerate(grid):
            for col_idx, val in enumerate(row):
                color = self._colormap[val]
                left  = col_idx * self._cell_size
                top   = row_idx * self._cell_size
                right = left + self._cell_size
                bottom= top  + self._cell_size
                draw.rectangle([left, top, right, bottom], fill=color)

                if val & self._highlight_bit:
                    draw.rectangle(
                        [left, top, right, bottom],
                        outline="black",
                        width=max(1, self._cell_size // 5)
                    )

        return img

    def add_break(self) -> None:
        pass

    def save_frame(self, grid: List[List[int]], filepath: Optional[Path]=None) -> str:
        if filepath is None:
            filepath = self._filepath
        img = self._frame(grid)
        img.save(filepath)
        return f"Visualization saved to {filepath}"

    def add_frame(self, grid: List[List[int]]):
        frame_img = self._frame(grid)
        self._frames.append(frame_img)

    def save_output(self, filepath: Optional[Path]=None, duration: int=500) -> str:
        if filepath is None:
            filepath = self._filepath
        if filepath.name == "image.jpg":
            filepath = Path.cwd() / "image.gif"
        if self._frames:
            self._frames[0].save(
                filepath,
                save_all=True,
                append_images=self._frames[1:],
                loop=0,
                duration=duration
            )
        return f"Visualization saved to {filepath}"
