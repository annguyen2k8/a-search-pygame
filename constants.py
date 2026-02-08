import pygame
from pygame import Color

pygame.font.init()
FONT = pygame.Font("./assets/font.otf", 16)


class Colors:
    BLACK = Color(20, 20, 20)
    WHITE = Color(255, 255, 255)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
