import math

from exceptions import SizeError
from vector import Vector


class Matrix:
    def __init__(self, vectors: list[Vector]):
        self._vectors: list(Vector) = []
        self.vectors = vectors
        self._size: tuple[int] = ()

    @property
    def vectors(self) -> list[Vector]:
        """Get the list of vectors.

        Returns:
            list[Vector]: _description_
        """
        return self._vectors

    @vectors.setter
    def vectors(self, vectors: list[Vector]) -> None:
        """Set the list of vectors.

        Args:
            vectors: _description_

        Raises:
            TypeError: Type of vectors must be list[Vector].
        """
        if not (
            isinstance(vectors, list[Vector])
            and all(isinstance(vector, Vector) for vector in vectors)
        ):
            raise TypeError("Type of vectors must be list[Vector].")
        self._vectors = vectors
