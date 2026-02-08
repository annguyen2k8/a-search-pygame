from typing import Callable, List, Optional

from pygame.typing import IntPoint

from core.cell import Cell, CellType


class Board:
    __width: int
    __height: int

    __cells: List[Cell]

    __start_pos: Optional[IntPoint]
    __goal_pos: Optional[IntPoint]

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

        self.__cells = []

        self.__start_pos = None
        self.__goal_pos = None

        for x in range(width):
            for y in range(height):
                self.__cells.append(Cell(x, y))

    @property
    def size(self) -> IntPoint:
        return (self.width, self.height)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def cells(self) -> List[Cell]:
        return self.__cells

    @property
    def start_pos(self) -> Optional[IntPoint]:
        return self.__start_pos

    @start_pos.setter
    def start_point(self, value: Optional[IntPoint]):
        if value and self.goal_pos == value:
            return

        self.__start_pos = value

    @property
    def goal_pos(self) -> Optional[IntPoint]:
        return self.__goal_pos

    @goal_pos.setter
    def goal_pos(self, value: Optional[IntPoint]):
        if value and self.start_point == value:
            return

        self.__goal_pos = value

    def foreach_cell(self, callback: Callable[[Cell, CellType], None]):
        for cell in self.cells:
            callback(cell, cell.cell_type)

    def get_cell_at(self, pos: IntPoint) -> Optional[Cell]:
        x, y = pos

        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def set_cell_type_at(self, pos: IntPoint, value: CellType):
        if pos in (self.start_point, self.goal_pos):
            return

        cell = self.get_cell_at(pos)
        if cell is not None:
            cell.set_type(value)
