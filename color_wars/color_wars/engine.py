from typing import Type, List, Tuple, Dict, Any
from players.player import Player
import copy
import json

class ColorWarsResult:
    def __init__(self, scores: Dict[str, float]):
        self.scores = scores

    def print_result(self) -> None:
        header_player = "Player"
        header_score = "Score"

        player_col_width = max(len(header_player),
                              max(len(player) for player in self.scores))
        score_strings = [f"{v:.4f}" for v in self.scores.values()]
        score_col_width = max(len(header_score),
                              max(len(s) for s in score_strings))

        border = (
            f"+{'-' * (player_col_width + 2)}+"
            f"{'-' * (score_col_width + 2)}+"
        )

        def make_row(col1: str, col2: str) -> str:
            return (
                f"| {col1.ljust(player_col_width)} "
                f"| {col2.rjust(score_col_width)} |"
            )

        print(border)
        print(make_row(header_player.center(player_col_width),
                       header_score.center(score_col_width)))
        print(border)

        for player, score in sorted(self.scores.items(),
                                   key=lambda kv: kv[1],
                                   reverse=True):
            print(make_row(player, f"{score:.4f}"))

        print(border)

class ColorWarsEngine:
    @staticmethod
    def run_game(players: List[Tuple[str, Player]], grid_size: int) -> Tuple[Dict[str, float], List[Dict[str, Any]]]:
        num_players = len(players)
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        player_bits = [2 ** i for i in range(num_players)]

        is_valid_cell = lambda x, y: 0 <= x < grid_size and 0 <= y < grid_size

        time = 0
        board = [[0] * grid_size for _ in range(grid_size)]
        board_times = [[-1] * grid_size for _ in range(grid_size)]
        history = []
        turns = []

        scores = [0.] * num_players
        while True:
            time += 1
            moves = [None] * num_players
            temp_board = copy.deepcopy(board)
            temp_history = copy.deepcopy(history)
            all_pass = True
            for i in range(num_players):
                move = players[i][1].play(temp_board, temp_history)

                x, y = move
                if not is_valid_cell(x, y) or (board_times[x][y] != time and board_times[x][y] != -1):
                    raise ValueError(f"Invalid move {move} made by {players[i][0]}.")

                moves[i] = move
                board[x][y] |= player_bits[i]
                board_times[x][y] = time
                all_pass = False
            history.append(moves)
            turns.append({"time": time, "allMoves": moves})

            temp_board = copy.deepcopy(board)
            empty_cells = 0
            scores = [0.] * num_players
            for x in range(grid_size):
                for y in range(grid_size):
                    if temp_board[x][y] == 0:
                        color = 0
                        for dx, dy in dirs:
                            nx, ny = x + dx, y + dy
                            if not is_valid_cell(nx, ny) or temp_board[nx][ny] not in player_bits:
                                continue
                            color |= temp_board[nx][ny]
                        if color == 0:
                            empty_cells += 1
                        else:
                            board[x][y] = color
                            board_times[x][y] = time
                    k = bin(board[x][y]).count("1")
                    for i in range(num_players):
                        if (board[x][y] >> i) & 1 == 1:
                            scores[i] += 1 / k

            if empty_cells == 0 or all_pass:
                break

        scores = {player_name: scores[i] / (grid_size ** 2) for i, (player_name, _) in enumerate(players)}
        return scores, turns

    @staticmethod
    def grade(player_classes: List[Tuple[str, Type[Player]]], grid_size: int, num_games: int, my_index: int = 0, feedback_out: str = "feedback.json") -> ColorWarsResult:
        scores = {player_name: 0 for player_name, _ in player_classes}
        num_players = len(player_classes)

        feedback = {
            "feedback": {
                "meta": {
                    "gridSize": grid_size,
                    "numPlayers": num_players,
                    "playerIndex": my_index,
                },
                "games": []
            }
        }

        # Simulate games
        for _ in range(num_games):
            players = [(player_name, player_class(player_index=i, grid_size=grid_size, num_players=num_players)) for i, (player_name, player_class) in enumerate(player_classes)]

            game_scores, turns = ColorWarsEngine.run_game(players, grid_size)

            feedback["feedback"]["games"].append({"turns": turns})

            for player_name, game_score in game_scores.items():
                scores[player_name] += game_score
                
        with open(feedback_out, 'w') as f:
            f.write(json.dumps(feedback, indent=2))

        scores = {player_name: score / num_games for player_name, score in scores.items()}
        return ColorWarsResult(scores)
