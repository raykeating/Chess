import numpy as np

# SAN_to_int - SAN is standard algebraic notation, the way pieces are represented in FEN strings.  
# this method converts the SAN character to the integer representation as used here. (used in parse_board in board.py)
def SAN_to_int(piece:str):
    pieces = [(1,'K'),(2,'k'),(3,'Q'),(4,'q'),(5,'B'),(6,'b'),(7,'N'),(8,'n'),(9,'R'),(10,'r'),(11,'P'),(12,'p')]
    for p in pieces:
        if piece == p[1]:
            return p[0]
    return 0

def get_symbol(piece:int, invert_colors:bool):
    if piece == 0:
        return ' '
    pieces = [(1,'\u2654'),(2,'\u265A'),(3,'\u2655'),(4,'\u265B'),(5,'\u2657'),(6,'\u265D'),
    (7,'\u2658'),(8,'\u265E'),(9,'\u2656'),(10,'\u265C'),(11,'\u2659'),(12,'\u265F')]
    if invert_colors:
        pieces = [(1,'\u265A'),(2,'\u2654'),(3,'\u265B'),(4,'\u2655'),(5,'\u265D'),(6,'\u2657'),
    (7,'\u265E'),(8,'\u2658'),(9,'\u265C'),(10,'\u2656'),(11,'\u265F'),(12,'\u2659')]
    for p in pieces:
        if piece == p[0]:
            return p[1]
    return ValueError("That is an invalid piece")

class BoardState:
    # board - an 8x8 numpy array representing the actual pieces on the board.  Pieces are represented as integers. 
    board = None
    next_move = None # nextMove - 0 or 1.  Indicates who's move it is.  (0 for black, 1 for white)

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
                print(get_symbol(self.board[i][j], invert_colors), end=" | ")
            print("\n  ---------------------------------")
        print("    A   B   C   D   E   F   G   H ")

    def fen_to_board_state(self, fen:str):

        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 -> fen for starting position

        board = fen.split(' ')[0]
        self.board = self.parse_board(board)
        self.next_move = 1 if fen.split(' ')[1] == 'w' else 0

    def parse_board(self, board:str):
        fen_ranks = board.split('/')
        int_ranks = []
        for rank in fen_ranks:
            # This for loop basically says "if the piece is a piece", convert to its integer representation.
            # otherwise, fill the empty tiles indicated by the int value in the FEN
            int_rank = []
            for piece in rank:
                if piece in "PRNBKQprnbkq":
                    int_rank.append(SAN_to_int(piece))
                elif piece in "12345678" and int(piece) > 0 and int(piece) < 9:
                    for i in range(int(piece)):
                        int_rank.append(0)
                else:
                    return ValueError("The FEN string may be invalid")

            int_ranks.append(int_rank)
            int_rank = []
            
            

        # return numpy array of the ranks.
        return np.array(int_ranks)

    def legal_pawn_moves(self, color, rank, file):
        legal_moves = []
        
        # LEGAL MOVES FOR WHITE
        if color == 'w':
            # allows pawns to move 2 squares on their first move.
            if rank == 6 and self.board[4][file] == 0:
                legal_moves.append((4, file))
        
            # if the square infront of a pawn is empty, it can move there
            try:
                if self.board[rank-1][file] == 0:
                    legal_moves.append(((rank-1), file))
            except IndexError:
                pass

            # check if left or right diagonal captures are possible
            try:
                if self.board[rank-1][file+1] != 0 and self.board[rank-1][file+1] % 2 == 0:
                    legal_moves.append(((rank-1),(file+1)))
            except IndexError:
                pass

            try:
                if self.board[rank-1][file-1] != 0 and self.board[rank-1][file-1] % 2 == 0:
                    legal_moves.append(((rank-1),(file-1)))
            except IndexError:
                pass
        
        # LEGAL MOVES FOR BLACK
        elif color == 'b':
            # allows pawns to move 2 squares on their first move.
            if rank == 1 and self.board[3][file] == 0: #check if indexing is right here
                legal_moves.append((3, file))
            
            # if the square infront of a pawn is empty, it can move there
            if self.board[rank+1][file] == 0:
                legal_moves.append(((rank+1), file))

            # check if left or right diagonal captures are possible
            try:
                if self.board[rank+1][file+1] != 0 and self.board[rank+1][file+1] % 2 == 1:
                    legal_moves.append(((rank+1),(file+1)))
            except IndexError:
                pass

            try:
                if self.board[rank+1][file-1] != 0 and self.board[rank+1][file-1] % 2 == 1:
                    legal_moves.append(((rank+1),(file-1)))
            except IndexError:
                pass

        else:
            return ValueError("wrong color argument")
        return legal_moves

    def legal_rook_moves(self, color, rank, file):
        
        legal_moves = []

        # downwards
        counter = 1
        while rank+counter < 8:
            if self.board[rank + counter][file] == 0:
                legal_moves.append((rank+counter,file))
            elif color == 'w' and self.board[rank + counter][file] % 2 == 0:
                legal_moves.append((rank+counter,file))
                break
            elif color == 'b' and self.board[rank + counter][file] % 2 == 1:
                legal_moves.append((rank+counter,file))
                break
            else:
                break
            counter += 1

        # upwards
        counter = 1
        while rank-counter > -1:
            if self.board[rank - counter][file] == 0:
                legal_moves.append((rank-counter,file))
            elif color == 'w' and self.board[rank - counter][file] % 2 == 0:
                legal_moves.append((rank-counter,file))
                break
            elif color == 'b' and self.board[rank - counter][file] % 2 == 1:
                legal_moves.append((rank-counter,file))
                break
            else:
                break
            counter += 1
        
        # right
        counter = 1
        while file+counter < 8:
            if self.board[rank][file + counter] == 0:
                legal_moves.append((rank,(file+counter)))
            elif color == 'w' and self.board[rank][file + counter] % 2 == 0:
                legal_moves.append((rank,(file+counter)))
                break
            elif color == 'b' and self.board[rank][file + counter] % 2 == 1:
                legal_moves.append((rank,(file+counter)))
                break
            else:
                break
            counter += 1

        # left
        counter = 1
        while file-counter > -1:
            if self.board[rank][file - counter] == 0:
                legal_moves.append((rank,(file-counter)))
            elif color == 'w' and self.board[rank][file - counter] % 2 == 0:
                legal_moves.append((rank,(file-counter)))
                break
            elif color == 'b' and self.board[rank][file - counter] % 2 == 1:
                legal_moves.append((rank,(file-counter)))
                break
            else:
                break
            counter += 1
            
        return legal_moves

    def legal_bishop_moves(self, color, rank, file):
        
        legal_moves = []

        # diagonal from piece to top-left
        counter = 1
        while True:
            try:
                if self.board[rank - counter][file - counter] == 0:
                    legal_moves.append((rank-counter,file-counter))
                elif color == 'w' and self.board[rank - counter][file - counter] % 2 == 0:
                    legal_moves.append((rank-counter,file-counter))
                    break
                elif color == 'b' and self.board[rank - counter][file - counter] % 2 == 1:
                    legal_moves.append((rank-counter,file-counter))
                    break
                else:
                    break
                counter += 1
            except IndexError:
                break
        
        # diagonal from piece to top-right
        counter = 1
        while True:
            try:
                if self.board[rank - counter][file + counter] == 0:
                    legal_moves.append((rank-counter,file+counter))
                elif color == 'w' and self.board[rank - counter][file + counter] % 2 == 0:
                    legal_moves.append((rank-counter,file+counter))
                    break
                elif color == 'b' and self.board[rank - counter][file + counter] % 2 == 1:
                    legal_moves.append((rank-counter,file+counter))
                    break
                else:
                    break
                counter += 1
            except IndexError:
                break
        
        # diagonal from piece to bottom-left
        counter = 1
        while True:
            try:
                if self.board[rank + counter][file + counter] == 0:
                    legal_moves.append((rank+counter,file+counter))
                elif color == 'w' and self.board[rank + counter][file + counter] % 2 == 0:
                    legal_moves.append((rank+counter,file+counter))
                    break
                elif color == 'b' and self.board[rank + counter][file + counter] % 2 == 1:
                    legal_moves.append((rank+counter,file+counter))
                    break
                else:
                    break
                counter += 1
            except IndexError:
                break
        
        # diagonal from piece to bottom-right
        counter = 1
        while True:
            try:
                if self.board[rank + counter][file - counter] == 0:
                    legal_moves.append((rank+counter,file-counter))
                elif color == 'w' and self.board[rank + counter][file - counter] % 2 == 0:
                    legal_moves.append((rank+counter,file-counter))
                    break
                elif color == 'b' and self.board[rank + counter][file - counter] % 2 == 1:
                    legal_moves.append((rank+counter,file-counter))
                    break
                else:
                    break
                counter += 1
            except IndexError:
                break

        return legal_moves

    def legal_knight_moves(self, color, rank, file):
        legal_moves = []
        offsets = [(2,1),(2,-1),(1,-2),(1,2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        for x, y in offsets:
            print(rank+x,file+y)
            try:
                if self.board[rank+x][file+y] == 0:
                    legal_moves.append((rank+x,file+y))
                elif color == 'w' and self.board[rank+x][file+y] % 2 == 0:
                    legal_moves.append((rank+x,file+y))
                elif color == 'b' and self.board[rank+x][file+y] % 2 == 1:
                    legal_moves.append((rank+x,file+y))
                else:
                    continue
            except IndexError:
                continue
        
        return legal_moves
        

