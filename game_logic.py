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
    
    # get_legal_moves takes a "gui_piece_info" argument (when called from the GUI class), which is a list representing the piece on the board.
    # the list has 3 elements, the first being the integer representation of the piece (0 to 12), the second being the surface (not used in this function), 
    # and the third being the pygame rect object. (which will be converted to array indices)
    def get_legal_moves(self, gui_piece_info:list):

        legal_moves = None

        # save the piece's integer representation (0 to 12) in piece
        piece = gui_piece_info[0]
        color = 'b' if piece % 2 == 0 else 'w'

        # convert the x, y values of the rect object to array indices representing the rank & file
        rank, file = int(gui_piece_info[2].y/100), int(gui_piece_info[2].x/100)

        if piece == 11 or piece == 12:
            legal_moves = self.board.legal_pawn_moves(color, rank, file)
            return legal_moves
        
        if piece == 9 or piece == 10:
            legal_moves = self.board.legal_rook_moves(color, rank, file)
            return legal_moves

        if piece == 7 or piece == 8:
            legal_moves = self.board.legal_knight_moves(color, rank, file)
            return legal_moves

        if piece == 5 or piece == 6:
            legal_moves = self.board.legal_bishop_moves(color, rank, file)
            return legal_moves
        
        if piece == 3 or piece == 4:
            legal_moves = self.board.legal_rook_moves(color, rank, file)
            legal_moves += self.board.legal_bishop_moves(color, rank, file)
            return legal_moves
        
        



