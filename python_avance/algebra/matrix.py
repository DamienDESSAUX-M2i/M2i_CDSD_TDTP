import math

from exceptions import EmptyError, SizeError
from vector import Vector


class Matrix:
    def __init__(self, vectors: list[Vector]):
        """Constructor.

        Args:
            vectors (list[Vector]): List of matirx lignes.
        """
        self._vectors: list(Vector) = []
        self.vectors = vectors

    @property
    def vectors(self) -> list[Vector]:
        """Get the list matirx lignes.

        Returns:
            list[Vector]: List of matirx lignes.
        """
        return self._vectors

    @vectors.setter
    def vectors(self, vectors: list[Vector]) -> None:
        """Set the list matirx lignes.

        Args:
            vectors: List of matirx lignes.

        Raises:
            TypeError: Type of vectors must be list[Vector].
            SizeError: Matrix lignes must have the same length.
        """
        if not (
            isinstance(vectors, list)
            and all(isinstance(vector, Vector) for vector in vectors)
        ):
            raise TypeError("Type of vectors must be list[Vector].")
        if vectors == []:
            raise EmptyError("A matrix must have at least one ligne.")
        first_vector_length = vectors[0].length
        if not all([vector.length == first_vector_length for vector in vectors]):
            raise SizeError("Matrix lignes must have the same length.")
        self._vectors = vectors

    @property
    def size(self) -> tuple[int]:
        """Get matrix size.

        Returns:
            tuple[int]: number of lignes then number of columns.
        """
        return (len(self.vectors), self.vectors[0].length)

    def __str__(self) -> str:
        strs: list[str] = []
        n, m = self.size
        for i in range(n):
            strs.append(f"[{', '.join([str(self[i][j]) for j in range(m)])}]")
        return f"[{';\n'.join(strs)}]"

    def __getitem__(self, key: int) -> Vector:
        """Get the k-th ligne of the matrix.

        Args:
            key (int): index ligne.

        Raises:
            TypeError: The type of key must be int.
            IndexError: key must be between 0 and the number of lignes minus 1.

        Returns:
            Vector: k-th ligne of the matrix.
        """
        if not isinstance(key, int):
            raise TypeError("The type of key must be int.")
        n, _ = self.size
        if (key < 0) or (key > n - 1):
            raise IndexError(f"key must be between 0 and {n - 1}")
        return self.vectors[key]

    def __add__(self, other: "Matrix") -> "Matrix":
        """Compute the sum of two matrix that have the same size.

        Args:
            other (Matrix): Matrix that have the same size.

        Raises:
            TypeError: The type of other must be Matrix.
            SizeError: Both matrix must have the same size.

        Returns:
            Matrix: Sum of two matrix that have the same size.
        """
        if not isinstance(other, Matrix):
            raise TypeError("The type of other must be Matrix.")
        if self.size != other.size:
            raise SizeError("Both matrix must have the same size.")
        return Matrix(
            [vector1 + vector2 for vector1, vector2 in zip(self.vectors, other.vectors)]
        )

    def __sub__(self, other: "Matrix") -> "Matrix":
        """Compute the difference of two matrix that have the same size.

        Args:
            other (Matrix): Matrix that have the same size.

        Raises:
            TypeError: The type of other must be Matrix.
            SizeError: Both matrix must have the same size.

        Returns:
            Matrix: Difference of two matrix that have the same size.
        """
        if not isinstance(other, Matrix):
            raise TypeError("The type of other must be Matrix.")
        if self.size != other.size:
            raise SizeError("Both matrix must have the same size.")
        return Matrix(
            [vector1 - vector2 for vector1, vector2 in zip(self.vectors, other.vectors)]
        )

    def __mul__(self, scalar: float) -> "Matrix":
        """Compute the multiplication of the matrix by a scalar.

        Args:
            other (Matrix): Matrix that have the same size.

        Raises:
            TypeError: The type of scalar must be float.

        Returns:
            Matrix: Multiplication of the matrix by a scalar.
        """
        if not isinstance(scalar, float):
            raise TypeError("The type of scalar must be float.")
        return Matrix([vector * scalar for vector in self.vectors])

    def transpose(self) -> "Matrix":
        """Transpose the martix.

        Returns:
            Matrix: Matrix transposed.
        """
        n, m = self.size
        return Matrix([Vector([self[i][j] for i in range(n)]) for j in range(m)])

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """Compute the matrix product of two matrix.

        Args:
            other (Matrix): Matrix with the number of lignes equals to the number of colums of the main matrix.

        Raises:
            TypeError: The type of other must be Matrix.
            SizeError: The number of lignes of the matrix must be equals to the numbre of lignes of the main matrix.

        Returns:
            Matrix: Sum of two matrix that have the same size.
        """
        if not isinstance(other, Matrix):
            raise TypeError("The type of other must be Matrix.")
        if self.size[1] != other.size[0]:
            raise SizeError(
                "The number of lignes of the matrix must be equals to the numbre of lignes of the main matrix."
            )
        other_transpose = other.transpose()
        return Matrix(
            [
                Vector(
                    [
                        vector.dot_product(vector_other)
                        for vector_other in other_transpose.vectors
                    ]
                )
                for vector in self.vectors
            ]
        )

    def __pow__(self, power: int) -> "Matrix":
        if not isinstance(power, int):
            raise TypeError("The type of power must be int.")
        if power < 0:
            raise ValueError("power must be greater than or equals to 0.")
        n, m = self.size
        if n != m:
            raise SizeError("The matrix must be squared.")
        if power == 0:
            return Matrix.ones(n, n)
        power_matrix = self
        for k in range(power):
            power_matrix = power_matrix @ self
        return power_matrix


if __name__ == "__main__":
    matrix1 = Matrix(
        [Vector([2.0, 0.0, 0.0]), Vector([0.0, 3.0, 0.0]), Vector([0.0, 0.0, -1.0])]
    )
    print("str : ", matrix1, "\n")
    print("getitem : ", matrix1[0], "\n")
    matrix2 = Matrix(
        [Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]), Vector([1.0, 0.0, 0.0])]
    )
    print("add : ", matrix1 + matrix2, "\n")
    print("sub : ", matrix1 - matrix2, "\n")
    print("mul : ", matrix1 * 2.0, "\n")
    matrix3 = Matrix([Vector([2.0, 0.0, 0.0]), Vector([0.0, 3.0, 0.0])])
    print("transpose : ", matrix3.transpose(), "\n")
    matrix4 = Matrix([Vector([0.0, 1.0]), Vector([1.0, 0.0]), Vector([1.0, 1.0])])
    print("matmul", matrix3 @ matrix4, "\n")
    print("pow : ", matrix1**2)
