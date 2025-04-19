from config import *
from engine import BidEngine

if __name__ == "__main__":
    grading_result = BidEngine.grade(player_classes, num_games)
    grading_result.print_result()
