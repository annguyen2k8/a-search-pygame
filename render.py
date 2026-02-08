from pygame import Surface, Rect
from pygame.typing import ColorLike, Point

from constants import FONT


class Render:
    @staticmethod
    def text(surface: Surface, color: ColorLike, text: str, dest: Point) -> Rect:
        return surface.blit(FONT.render(text, True, color), dest)
