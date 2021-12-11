from board import BoardState
import pieces

class Game:

    # board, represents a board state but simplified to board
    board = None

    def __init__(self):
        self.board = BoardState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def move_piece(self, move:str):
        # moves are defined as a tuple of squares (squares are written in algebraic notation).   
        # The first value is the location of the selected piece to move, 
        # the second value is the location of the desired move.  For example, (g1,f3)

        # first, get the array indexes of the selected piece, and the desired location for that move.
        sel_index = ((8-int(move[1])), ord(move[0])-97)
        des_index = ((8-int(move[3])), ord(move[2])-97)
        self.board.printb(True)
        print(self.board.board[7][0])
        print(sel_index, " | ", des_index)



