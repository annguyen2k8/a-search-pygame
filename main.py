import pygame
from pygame.locals import *

pygame.init()

FONT = pygame.Font("./assets/font.otf")

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)

def render_text(text, color):
    return FONT.render(text, True, color)

def main():
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BLACK)
        
        text = render_text(f"{clock.get_fps():.0f} FPS", WHITE)
        
        screen.blit(text, (5, 5))
           
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise error