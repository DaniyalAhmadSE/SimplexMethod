from models.point import Point


class Point2D(Point):
    def __init__(self, x=0, y=0, dimensions: int = 2) -> None:
        super().__init__(dimensions)
        self.set_coord(x, 0)
        self.set_coord(y, 1)

    def get_x(self) -> float:
        return self.get_coord(0)

    def set_x(self, x: float) -> None:
        self.set_coord(x, 0)

    def get_y(self) -> float:
        return self.get_coord(1)

    def set_y(self, y: float) -> None:
        self.set_coord(y, 1)

    x: float = property(get_x, set_x)
    y: float = property(get_y, set_y)
