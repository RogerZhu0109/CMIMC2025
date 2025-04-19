from typing import Dict, Tuple, List, Type, Any
from players.player import Player
from collections import defaultdict
import random

class BidResult:
    def __init__(self, scores: Dict[str, float]):
        self.scores = scores

    def print_result(self) -> None:
        header_player = "Player"
        header_score = "Average Score"
        player_col_width = max(len(header_player), max(len(player) for player in self.scores.keys()))
        score_col_width = max(len(header_score), max(len(str(score)) for score in self.scores.values()))
        
        border = f"+{'-' * (player_col_width + 2)}+{'-' * (score_col_width + 2)}+"
        header = f"| {header_player.ljust(player_col_width)} | {header_score.rjust(score_col_width)} |"
        
        print(border)
        print(header)
        print(border)
        
        for player, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            print(f"| {player.ljust(player_col_width)} | {str(score).rjust(score_col_width)} |")
        
        print(border)

class BidEngine:
    @staticmethod
    def _filter_unique(L: List[Any]) -> List[Any]:
        freq = defaultdict(lambda: 0)
        for x in L:
            freq[x] += 1
        return [x for x, count in freq.items() if count == 1]

    @staticmethod
    def run_game(players: List[Tuple[str, Player]]) -> Dict[str, int]:
        scores = {player_name: 0 for player_name, _ in players}
        player_history = [[] for _ in range(len(players))]

        score_cards = list(range(-5, 0)) + list(range(1, 11))
        random.shuffle(score_cards)

        for score_card in score_cards:
            bids = []
            for i, (player_name, player) in enumerate(players):
                bid = player.play(score_card, player_history)

                if bid in player_history[i] or bid not in set(range(1, 16)):
                    raise ValueError(f"Invalid bid {bid} made by {player_name}.")

                bids.append(bid)

            for i, bid in enumerate(bids):
                player_history[i].append(bid)

            unique_bids = sorted(BidEngine._filter_unique(bids))
            if len(unique_bids) == 0:
                continue

            if score_card > 0:
                winner_index = bids.index(unique_bids[-1])
            else:
                winner_index = bids.index(unique_bids[0])

            scores[players[winner_index][0]] += score_card

        return scores

    @staticmethod
    def grade(player_classes: List[Tuple[str, Type[Player]]], num_games: int = 100) -> BidResult:
        scores = {player_name: 0 for player_name, player_class in player_classes}

        # Simulate games
        for _ in range(num_games):
            players = [(player_name, player_class(player_index=i)) for i, (player_name, player_class) in enumerate(player_classes)] # Initialize with player index
            game_scores = BidEngine.run_game(players)
            for player_name, game_score in game_scores.items():
                scores[player_name] += game_score

        scores = {player_name: score / num_games for player_name, score in scores.items()}
        return BidResult(scores)
