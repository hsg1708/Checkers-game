import pygame

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255,0,0)
WHITE =(200,160,140)
BLACK = (0,0,0)
BLUE = (120,121,110)
GREY = (128,128,128)


CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
