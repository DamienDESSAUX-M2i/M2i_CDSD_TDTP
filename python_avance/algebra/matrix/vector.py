import math

from matrix.exceptions import EmptyError, SizeError


class Vector:
    def __init__(self, coordinates: list[float]):
        """Constructor.

        Args:
            coordinates (list[float]): List of vector coordinates.
        """
        self._coordinates: list[float] = [0.0]
        self.coordinates = coordinates

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
            TypeError: Type of 'coordinates' must be list[float].
            EmptyError: "A vector must have at least one coordinate."
        """
        if not (
            isinstance(coordinates, list)
            and all(isinstance(coordinate, float) for coordinate in coordinates)
        ):
            raise TypeError("Type of 'coordinates' must be list[float].")
        if coordinates == []:
            raise EmptyError("A vector must have at least one coordinate.")
        self._coordinates = coordinates

    @property
    def length(self) -> int:
        """Get length of the vector.

        Returns:
            int: Length of the vector.
        """
        return len(self._coordinates)

    def __str__(self) -> str:
        """str method.

        Returns:
            str: Coordinates of the vector.
        """
        return f"[{';\n'.join([str(x) for x in self.coordinates])}]"

    def __getitem__(self, key: int) -> float:
        """Get the k-th coordinate of the vector.

        Args:
            key (int): index coordinate.

        Raises:
            TypeError: The type of 'key' must be int.
            IndexError: 'key' must be between 0 and the length of the vector minus one.

        Returns:
            float: k-th coordinate of the vector.
        """
        if not isinstance(key, int):
            raise TypeError("The type of 'key' must be int.")
        if (key < 0) or (key > self.length - 1):
            raise IndexError(f"'key' must be between 0 and {self.length - 1}")
        return self.coordinates[key]

    def __setitem__(self, key: int, coordinate: float) -> None:
        """Set the k-th coordinate of the vector.

        Args:
            key (int): index coordinate.
            coordinate (float): k-th coordinate of the vector

        Raises:
            TypeError: The type of 'key' must be int.
            IndexError: 'key' must be between 0 and the length of the vector minus one.
            TypeError: The type of 'coordinate' must be float.
        """
        if not isinstance(key, int):
            raise TypeError("The type of 'key' must be int.")
        if (key < 0) or (key > self.length - 1):
            raise IndexError(f"'key' must be between 0 and {self.length - 1}")
        if not isinstance(coordinate, float):
            raise TypeError("The type of 'coordinate' must be float.")
        self.coordinates[key] = coordinate

    def __eq__(self, other: "Vector") -> bool:
        """Compare two vectors.

        Args:
            other (Vector): Vector to compare.

        Returns:
            bool: True if both vectors have the same length and same coordinates, False overwise.
        """
        if self.length != other.length:
            return False
        for k in range(self.length):
            if self[k] != other[k]:
                return False
        return True

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
        """Multiply a vector by a scalar.

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
                - self.coordinates[2] * other.coordinates[1],
                self.coordinates[0] * other.coordinates[2]
                - self.coordinates[2] * other.coordinates[0],
                self.coordinates[0] * other.coordinates[1]
                - self.coordinates[1] * other.coordinates[0],
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
        if p == 1:
            return sum([abs(x) for x in self.coordinates])
        return math.exp(
            math.log(sum([math.pow(abs(x), p) for x in self.coordinates])) / p
        )

    @property
    def norm_1(self) -> float:
        """Compute the norm 1 of the vector.

        Returns:
            float: Norm 1 of the vector.
        """
        return self.norm_p(p=1)

    @property
    def norm_2(self) -> float:
        """Compute the norm 2 of the vector.

        Returns:
            float: Norm 2 of the vector.
        """
        return self.norm_p(p=2)

    @property
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
        if self.dot_product(other=other) == 0.0:
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

    @classmethod
    def ones(cls, n: int) -> "Vector":
        """Create a vector full of 1.

        Args:
            n (int): Length of the vector.

        Raises:
            TypeError: The type of 'n' must be int.
            ValueError: 'n' must be greater than or equals to 1.

        Returns:
            Vector: Vector full of 1.
        """
        if not isinstance(n, int):
            raise TypeError("The type of 'n' must be int.")
        if n < 1:
            raise ValueError("'n' must be greater than or equals to 1.")
        return Vector([1.0 for i in range(n)])

    @classmethod
    def zeros(cls, n: int) -> "Vector":
        """Create a vector full of 0.

        Args:
            n (int): Length of the vector.

        Raises:
            TypeError: The type of 'n' must be int.
            ValueError: 'n' must be greater than or equals to 1.

        Returns:
            Vector: Vector full of 0.
        """
        if not isinstance(n, int):
            raise TypeError("The type of 'n' must be int.")
        if n < 1:
            raise ValueError("'n' must be greater than or equals to 1.")
        return Vector([0.0 for i in range(n)])


if __name__ == "__main__":
    vector1 = Vector([1.0, 0.0, 2.0])
    vector2 = Vector([-3.0, 0.5, 1.5])
    print("getitem : ", vector1[0], "\n")
    vector1[1] = -1.0
    print("setitem : ", vector1[1], "\n")
    print("add : ", vector1 + vector2, "\n")
    print("sub : ", vector1 - vector2, "\n")
    print("mul : ", vector1 * 2.0, "\n")
    print("dot_product : ", vector1.dot_product(vector2), "\n")
    print("is_orthogonal : ", vector1.is_orthogonal(vector2), "\n")
    print("vector_product : ", vector1.vector_product(vector2), "\n")
    print("is collonear : ", vector1.is_collinear(vector1), "\n")
    print("norm_1 : ", vector1.norm_1, "\n")
    print("norm_2 : ", vector1.norm_2, "\n")
    print("norm_infinity : ", vector1.norm_infinity, "\n")
    vector1.normalisation(p=0)
    print("normalisation : ", vector1.norm_infinity, "\n")
    print("ones : ", vector1.ones(3), "\n")
    print("zeros : ", vector1.zeros(2), "\n")
