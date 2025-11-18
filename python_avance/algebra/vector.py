import math

from exceptions import SizeError


class Vector:
    def __init__(self, coordinates: list[float]):
        """Constructor"""
        self._coordinates: list[float] = []
        self.coordinates = coordinates
        self._length: int = 0
        self.length = len(coordinates)

    @property
    def coordinates(self) -> list[float]:
        """Get coordinates of the vector.

        Returns:
            list[float]: Coordinates of the vector.
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates: list[float]) -> None:
        """Set coordinates of the vector.

        Args:
            coordinates: Coordinates of the vector.

        Raises:
            TypeError: Type of coordinates must be list[float].
        """
        if not (
            isinstance(coordinates, list)
            and all(isinstance(float, coordinate) for coordinate in coordinates)
        ):
            raise TypeError("Type of coordinates must be list[float].")
        self._coordinates = coordinates

    @property
    def length(self) -> int:
        """Get length of the vector.

        Returns:
            int: Length of the vector.
        """
        return self._length

    @length.setter
    def length(self, length: int) -> None:
        """Set length of the vector.

        Args:
            length: Length of the vector.

        Raises:
            TypeError: Type of length must be int.
        """
        if not isinstance(length, int):
            raise TypeError("Type of length must be int.")
        self._length = length

    def __add__(self, other: "Vector") -> "Vector":
        """Add two vectors.

        Args:
            other (Vector): Vector to add.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: Vector sum
        """
        if not isinstance(other, Vector):
            raise TypeError("Type of other must be Vector.")
        if self.length != other.length:
            raise SizeError("The two vectors must have the same length.")
        return Vector(
            coordinates=[x + y for x, y in zip(self.coordinates, other.coordinates)]
        )

    def __sub__(self, other: "Vector") -> "Vector":
        """Add two vectors.

        Args:
            other (Vector): Vector to substract.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: Vector difference.
        """
        if not isinstance(other, Vector):
            raise TypeError("Type of other must be Vector.")
        if self.length != other.length:
            raise SizeError("The two vectors must have the same length.")
        return Vector(
            coordinates=[x - y for x, y in zip(self.coordinates, other.coordinates)]
        )

    def __mul__(self, scalar: float) -> "Vector":
        """Multiply a vector by a scalar..

        Args:
            scalar (float): Scalar that multiplies the vector.

        Raises:
            TypeError: Type of other must be Vector.

        Returns:
            Vector: Vector multiplied by a scalar.
        """
        if not isinstance(scalar, float):
            raise TypeError("Type of scalar must be float.")
        return Vector(coordinates=[scalar * x for x in self.coordinates])

    def dot_product(self, other: "Vector") -> float:
        """Compute the dot product of two vectors.

        Args:
            other (Vector): Vector of the same length.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: Dot product of two vectors.
        """
        if not isinstance(other, Vector):
            raise TypeError("Type of other must be Vector.")
        if self.length != other.length:
            raise SizeError("The two vectors must have the same length.")
        return sum([x * y for x, y in zip(self.coordinates, other.coordinates)])

    def vector_product(self, other: "Vector") -> "Vector":
        """Compute the vector product of two vectors.

        Args:
            other (Vector): Vector of the same length.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: Dot product of two vectors.
        """
        if not isinstance(other, Vector):
            raise TypeError("Type of other must be Vector.")
        if (self.length != 3) or (other.length != 3):
            raise SizeError("Both vectors must have a length of 3.")
        return Vector(
            coordinates=[
                self.coordinates[1] * other.coordinates[2]
                - other.coordinates[2] * self.coordinates[1],
                self.coordinates[0] * other.coordinates[2]
                - other.coordinates[2] * self.coordinates[0],
                self.coordinates[0] * other.coordinates[1]
                - other.coordinates[1] * self.coordinates[0],
            ]
        )

    def norm_p(self, p: int) -> float:
        """Compute the norm p of the vector. Note that p=0 corresponds to the infinite norm.

        Args:
            p (int): Index norm. Note that p=0 corresponds to the infinite norm.

        Raises:
            TypeError: The type of p must be int.
            ValueError: p must be greather than or equal to 0.

        Returns:
            float: Norm p of the vector.
        """
        if not isinstance(p, int):
            raise TypeError("The type of p must be int.")
        if p < 0:
            raise ValueError("p must be greather than or equal to 0.")
        if p == 0:
            return max([abs(x) for x in self.coordinates])
        return math.exp(
            math.log(sum([math.pow(abs(x), p) for x in self.coordinates])) / p
        )

    def norm_1(self) -> float:
        """Compute the norm 1 of the vector.

        Returns:
            float: Norm 1 of the vector.
        """
        return self.norm_p(p=1)

    def norm_2(self) -> float:
        """Compute the norm 2 of the vector.

        Returns:
            float: Norm 2 of the vector.
        """
        return self.norm_p(p=2)

    def norm_infinity(self) -> float:
        """Compute the infinity norm of the vector.

        Returns:
            float: Infinity norm of the vector.
        """
        return self.norm_p(p=0)

    def normalisation(self, p: int) -> None:
        """Normalize a vector with the norm p.

        Args:
            p (int): norm index.
        """
        norm_p: float = self.norm_p(p=p)
        if norm_p != 0:
            self.coordinates = [x / norm_p for x in self.coordinates]

    def is_orthogonal(self, other: "Vector") -> bool:
        """Check if two vectors are orthogonal.

        Args:
            other (Vector): Vector of the same length.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: True if the vectors are orthogonal, False overwise.
        """
        if self.vector_product(other=other) == 0:
            return True
        return False

    def is_collinear(self, other: "Vector") -> bool:
        """Check if two vectors are collinear.

        Args:
            other (Vector): Vector of the same length.

        Raises:
            TypeError: Type of other must be Vector.
            SizeError: The two vectors must have the same length.

        Returns:
            Vector: True if the vectors are colinear, False overwise.
        """
        if not isinstance(other, Vector):
            raise TypeError("Type of other must be Vector.")
        if self.length != other.length:
            raise SizeError("The two vectors must have the same length.")
        for i in range(self.length):
            for j in range(i + 1, self.length):
                if (
                    self.coordinates[i] * other.coordinates[j]
                    != self.coordinates[j] * other.coordinates[i]
                ):
                    return False
        return True
