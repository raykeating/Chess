from model import BoardState
import copy

def evaluate(board:BoardState):
    # this function evaluates a given board state.  returns a positive "score" if black is winning, negative "score" if white is winning
    score = 0

    # the various piece values and associated integer codes
    # pawn value = 100, 11/12
    # bishop value = 300, 5/6
    # knight value = 300, 7/8
    # rook value = 500, 9/10
    # queen value = 900, 3/4
    piece_values = [(3,900),(4,900),(5,300),(6,300),(7,300),(8,300),(9,500),(10,500),(11,100),(12,100)]

    # add up the values of all of the pieces
    for rank in range(8):
        for file in range(8):
            if board.board[rank][file] != 0:
                if board.board[rank][file] > 2:
                    # gets the piece's value from the piece_values list
                    piece_value = [value[1] for value in piece_values if board.board[rank][file] == value[0]]
                    if board.board[rank][file] % 2 == 1: # if the piece is white
                        score -= piece_value[0]
                    else: # if the piece is black
                        score += piece_value[0]

    # give a slight score increase to a player in check to make the AI more aggressive.
    if board.in_check('w'):
        score += 30 
        if board.in_checkmate('w'):
            score = 10000
    elif board.in_check('b'):
        score -= 30 
        if board.in_checkmate('b'):
            score = -10000
            
    return score

# It just returns a board given the board in the parameter.
def get_board_from_move(board:BoardState, r1, f1, r2, f2):
    board = copy.deepcopy(board) # check if this 
    board.move_piece(r1, f1, r2, f2) # make sure this makes a copy
    return board

def get_next_moves(board:BoardState, player):
        # this function returns all possible boards one move ahead of the given board.
        # returns as a list of Board objects

        # player is a boolean used in the minimax algorithm.  It represents the maximizing player.
        # since black is always going to be the maximizing player, 
        # if player is True we will return the moves of the black player, 
        # if it is False we will return the moves of the white player.

        color = 'b' if player else 'w'

        all_legal_moves = board.get_all_legal_moves(color)

        # all_legal_moves = optimize_move_order(all_legal_moves, board, color)

        all_legal_boards = []
        for move in all_legal_moves:
            new_board = get_board_from_move(board, move[0][0], move[0][1], move[1][0], move[1][1])
            all_legal_boards.append(new_board)
        
        return all_legal_boards

def minimax(board, depth, alpha, beta, maximizing_player):
    # base case: if the depth limit has been reached or if the board is a winning board.
    score = evaluate(board)
    # print(board.board, "score: ", score)
    if depth == 0 or score == -10000 or score == 10000:
        return (score, board)
        
    # if it is the AI's move (the AI is trying to maximize their score)
    if maximizing_player:
        max_eval = -10001
        best_board = None
        # print('hello')
        # print(get_next_moves(board, maximizing_player))
        for move in get_next_moves(board, maximizing_player):
            # print('hello')
            # if depth == 2:
            #     print(move.board)
            eval = minimax(move,(depth-1), alpha, beta, False)
            if eval[0] >= max_eval:
                max_eval = eval[0]
                best_board = move
            alpha = max(alpha, eval[0])
            if beta <= alpha:
                break
        return (max_eval, best_board)
    
    # if it is the opponent's move (the AI is trying to minimize the opponent's score)
    else:
        min_eval = 10001
        best_board = None
        for move in get_next_moves(board, maximizing_player):
            eval = minimax(move, (depth-1), alpha, beta, True)
            if eval[0] <= min_eval:
                min_eval = eval[0]
                best_board = move
            beta = min(beta, eval[0])
            if beta <= alpha:
                break
        # if type(best_board) == None:
        #     best_board = self.place()
        return (min_eval, best_board)

    # The code for this algorithm is heavily inspired by Sebastian Lague's minimax video:
    # https://www.youtube.com/watch?v=l-hh51ncgDI

# def optimize_move_order(moves:list, board:BoardState, color):
#     # since A/B pruning's effectiveness can vary widely depending on the order of the moves searched, we we will try to optimize the order of the minimax search 
#     # by sorting the moves passed into the minimax search to find some moves that are generally good.  For example:
#     # -- when there is a capture of a high-value piece by a low-value piece, such as a pawn capturing a queen.

#     piece_values = [(3,900),(4,900),(5,300),(6,300),(7,300),(8,300),(9,500),(10,500),(11,100),(12,100)]
#     new_ordering = []
#     captures = []

#     print(moves)

#     for move in moves:
#         capturer_value = [value[1] for value in piece_values if value[0] == board.board[move[0][0]][move[0][1]]]
#         if board.board[move[1][0]][move[1][1]] > 2 and board.board[move[1][0]][move[1][1]] % 2 == color: # if the move is a capture, see how "good" of a capture it is
#             capturee_value = [value[1] for value in piece_values if value[0] == board.board[move[1][0]][move[1][1]]]
#             print('m', board.board[move[1][0]][move[1][1]],'c',board.board[move[1][0]][move[1][1]])
#             print(capturee_value, capturer_value)
#             relative_capture_value = capturee_value[0] - capturer_value[0]
#             captures.append((move, relative_capture_value))
#         else: # otherwise, just add it to new ordering.
#             new_ordering.append(move)
    
#     captures.sort(key=lambda x: x[1]) # sort catures by "relative_capture_value".
#     for capture in captures:
#         new_ordering.insert(0,capture[0]) # add the captures to the front of the list.

#     return new_ordering

            
