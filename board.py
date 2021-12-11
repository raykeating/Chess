from pieces import Pieces
import numpy as np

class BoardState:
    # board - an 8x8 numpy array representing the actual pieces on the board.  Pieces are represented as integers. 
    board = None
    next_move = None # nextMove - 'w' or 'b'.  Indicates who's move it is

    # castling = boolean array, index 0,1 indicate if white can castle kingside or queenside (respectively), 
    # index 2,3 indicate if black can castle kingside, queenside (respectively)
    castling = None

    # enPassant - an integer tuple with value (r,f): r is the rank, f is the integer value of the file
    en_passant = None
    
    # hm_clock, fm_clock - integers representing the halfmove clock and fullmove clock.  
    # halfmove is used for the fifty-move rule.
    hm_clock = None
    fm_clock = None

    # initialize a board state with a fen string
    def __init__(self, fen):
        self.fen_to_board_state(fen)


    def printb(self, invert_colors):
        print("  ---------------------------------")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if j == 0: print(f'{(8-i)} |', end=" ") 
                print(Pieces.get_symbol(self.board[i][j], invert_colors), end=" | ")
            print("\n  ---------------------------------")
        print("    A   B   C   D   E   F   G   H ")

    def fen_to_board_state(self, fen:str):

        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 -> fen for starting position

        board = fen.split(' ')[0]
        self.board = self.parse_board(board)
        self.next_move = fen.split(' ')[1]

    def parse_board(self, board:str):
        fen_ranks = board.split('/')
        int_ranks = []
        for rank in fen_ranks:
            # This for loop basically says "if the piece is a piece", convert to its integer representation.
            # otherwise, fill the empty tiles indicated by the int value in the FEN
            int_rank = []
            for piece in rank:
                if piece in "PRNBKQprnbkq":
                    int_rank.append(Pieces.SAN_to_int(piece))
                elif piece in "12345678" and int(piece) > 0 and int(piece) < 9:
                    for i in range(int(piece)):
                        int_rank.append(0)
                else:
                    return ValueError("The FEN string may be invalid")

            int_ranks.append(int_rank)
            int_rank = []
            
            

        # return numpy array of the ranks.
        return np.array(int_ranks)