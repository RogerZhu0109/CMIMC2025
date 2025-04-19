import json
from pathlib import Path
from typing import List, Optional, Type

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def _in_bounds(x: int, y: int, n: int) -> bool:
    return 0 <= x < n and 0 <= y < n

def _spread_once(board: List[List[int]], n: int, bits: List[int]) -> None:
    snapshot = [row[:] for row in board]
    for x in range(n):
        for y in range(n):
            if snapshot[x][y] != 0:
                continue
            colour = 0
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if _in_bounds(nx, ny, n) and snapshot[nx][ny] in bits:
                    colour |= snapshot[nx][ny]
            if colour:
                board[x][y] = colour


class FeedbackVisualizer:
    def __init__(
        self,
        feedback_path: Path,
        vis_cls: Type["AbstractVisualizer"],
        output_path: Optional[Path] = None,
        game_index: Optional[int] = None,
    ):
        fp = Path(feedback_path)
        data = json.loads(fp.read_text())

        self._games = data["feedback"]["games"]
        meta = data["feedback"]["meta"]
        self._N: int = meta["gridSize"]
        self._P: int = meta["numPlayers"]
        self._my_idx  = meta["playerIndex"]
        self._bits = [1 << i for i in range(self._P)]

        if game_index is not None:
            self._games = [self._games[game_index]]

        if output_path is None:
            default_ext = getattr(vis_cls, "default_extension", ".txt")
            output_path = fp.with_suffix(default_ext)
        self._vis = vis_cls(self._N, self._P, output_path, highlight_player=self._my_idx)

    def render(self) -> str:
        for gi, game in enumerate(self._games):
            board = [[0] * self._N for _ in range(self._N)]

            self._vis.add_frame(board)

            for turn in game["turns"]:
                before_spread = [row[:] for row in board]
                for i, move in enumerate(turn["allMoves"]):
                    if move is None:
                        continue
                    x, y = move
                    before_spread[x][y] |= self._bits[i]
                    board[x][y] |= self._bits[i]

                self._vis.add_frame(before_spread)

                _spread_once(board, self._N, self._bits)

                self._vis.add_frame(board)

            if gi < len(self._games) - 1:
                self._vis.add_break()

        return self._vis.save_output()
