import pygame

def setup_board(screen):

    dark_color = (48,29,10)
    light_color = (245,222,179)
    
    black_square = pygame.Surface((100,100))
    black_square.fill(dark_color)
    white_square = pygame.Surface((100,100))
    white_square.fill(light_color)

    for i in range(8):
        flip = 1
        if i % 2 == 0:
            flip = 0
        for j in range(8):
            if j % 2 == flip:
                screen.blit(black_square,(j*100,i*100))
            else:
                screen.blit(white_square,(j*100,i*100))

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    setup_board(screen)

    # main event loop
    while True:
        # enable close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # update display 144 times/sec
        pygame.display.update()
        clock.tick(144)