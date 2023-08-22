from typing import List


class Point:
    def __init__(self, dimensions) -> None:
        self._coords = [0]*dimensions

    def get_coords(self) -> List[float]:
        return self._coords

    def set_coord(self, coord: float, index: int) -> None:
        self._coords[index] = coord

    def get_coord(self, index: int) -> float:
        return self._coords[index]

    coords = property(get_coords)
