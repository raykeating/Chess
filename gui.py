import pygame
from game_logic import Game, BoardState

screen = pygame.display.set_mode((800,800))

def draw_board(board:BoardState):
    dark_color = "#EDEDD2"
    light_color = "#769459"
    
    black_square = pygame.Surface((100,100))
    black_square.fill(pygame.Color(dark_color))
    white_square = pygame.Surface((100,100))
    white_square.fill(pygame.Color(light_color))

    pieces = []
    for i in range(8):
        flip = 1
        if i % 2 == 0:
            flip = 0
        for j in range(8):
            # get the integer value of the piece
            pieceInt = board.board[i][j]

            # draw the background
            if j % 2 == flip:
                screen.blit(black_square,(j*100,i*100))
            else:
                screen.blit(white_square,(j*100,i*100))

            # draw the piece if it's not empty (0)
            if pieceInt > 0 and pieceInt < 13:
                pieceImg = pygame.image.load(f'Pieces/{pieceInt}.png')
                pieceImg = pygame.transform.smoothscale(pieceImg, (100,100))
                piece = pieceImg.get_rect(x=j*100, y=i*100)
                pieces.append((piece, pieceInt))
                screen.blit(pieceImg, piece)
                    
                    
    return pieces

def run_game():
    game = Game()

    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    pieces = draw_board(game.board)

    # main event loop
    while True:
        for event in pygame.event.get():
            # enable close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # listen for mousedown
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                clicked_piece = [p for p in pieces if p[0].collidepoint(pos1)]
                print(clicked_piece)
                # if the player clicked their own piece
                if clicked_piece[0][1] % 2 == game.next_move:
                    print('selected piece: ', clicked_piece)
                    
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    mouse_up = pygame.event.wait()
                    
                    print(mouse_up)
                    
                    pos2 = pygame.mouse.get_pos()
                    captured_piece = [p for p in pieces if p[0].collidepoint(pos2)]
                    if captured_piece:
                        if captured_piece[0][1] % 2 != game.next_move:
                            print("a piece was captured")
                            game.move_piece(pos1[0], pos1[1], pos2[0], pos2[1], clicked_piece[0][1])
                            pieces = draw_board(game.board)
                            game.next_move = 1 if game.next_move == 0 else 0
                        else:
                            print("you can't capture your own piece")
                    else:
                        game.move_piece(pos1[0], pos1[1], pos2[0], pos2[1], clicked_piece[0][1])
                        pieces = draw_board(game.board)
                        game.next_move = 1 if game.next_move == 0 else 0
                else:
                    print('that is not your piece')
                
                

            # listen for mouseup
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                


        # update display 144 times/sec
        pygame.display.update()
        clock.tick(144)