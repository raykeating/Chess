from board import BoardState
import math

class Game:

    # board represents a board state but simplified to board
    board = None
    next_move = None

    def __init__(self):
        self.board = BoardState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.next_move = self.board.next_move

    def move_piece(self, x1, y1, x2, y2, piece):   

        x1 = math.floor(x1/100)
        y1 = math.floor(y1/100)
        x2 = math.floor(x2/100)
        y2 = math.floor(y2/100)

        print(y1, x1, "|", y2, x2)

        self.board.board[y1][x1] = 0
        self.board.board[y2][x2] = piece
        



