import os
from datetime import datetime
from typing import Optional, Tuple


class MoveRecorder:
    def __init__(self, clear_file=False):
        self.moves = []
        self.filename = "reviews/review_moves.txt"
        # Only overwrite file if explicitly requested (for new games)
        os.makedirs("reviews", exist_ok=True)
        if clear_file:
            with open(self.filename, 'w') as f:
                pass

    def record_move(self, from_pos: Optional[Tuple[int, int]], to_pos: Tuple[int, int]):
        from_pixel = from_pos if from_pos else (0, 0)
        line = f"{from_pixel} {to_pos}"
        self.moves.append(line)
        with open(self.filename, 'a') as f:
            f.write(line + "\n")

    def reset_moves(self):
        # Overwrite the file and clear moves
        self.moves = []
        with open(self.filename, 'w') as f:
            pass

    def get_moves(self):
        # Read moves from file
        with open(self.filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
