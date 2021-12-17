from model import BoardState
import math
import ai

class Game:

    # board represents a board state but simplified to board
    board = None
    current_move = None

    def __init__(self):
        self.board = BoardState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
        self.current_move = self.board.current_move
    
    # get_legal_moves takes a "gui_piece_rect" argument (when called from the GUI class), which is a pygame rect object representing the piece's location
    # on the board.  In this function, we convert the rect object to array indices and call the get_legal_moves method in the BoardState class (in model)
    def get_legal_moves(self, gui_piece_rect):
        # convert the x, y values of the rect object to array indices representing the rank & file
        rank, file = int(gui_piece_rect.y/100), int(gui_piece_rect.x/100)

        # get the legal moves from the board class
        return self.board.get_legal_moves(rank, file)

    # move_piece as defined here takes GUI rect arguments instead of standard board indexes.
    def move_piece(self, r1, f1, r2, f2):   
        f1 = math.floor(f1/100)
        r1 = math.floor(r1/100)
        f2 = math.floor(f2/100)
        r2 = math.floor(r2/100)

        self.board.move_piece(r1,f1,r2,f2)
        self.current_move = self.board.current_move
        self.check_for_check()
        if self.board.white_in_check or self.board.black_in_check:
            self.check_for_checkmate()
        

    def move_piece_with_ai(self, depth):
        self.board = ai.minimax(self.board, depth, -10001, 10001, True)[1]
        self.current_move = 1 if self.current_move == 0 else 0 # change to next move

    def check_for_check(self):
        self.board.black_in_check = self.board.in_check('b')
        self.board.white_in_check = self.board.in_check('w')

    def check_for_checkmate(self):
        self.board.black_checkmated = self.board.in_checkmate('b')
        self.board.white_checkmated = self.board.in_checkmate('w')


