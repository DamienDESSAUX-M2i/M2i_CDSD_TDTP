import pytest
from matrix.exceptions import EmptyError, SizeError
from matrix.vector import Vector


class TestVector:
    """Test the class Vector."""

    # @classmethod
    # def setup_method(self):
    #     """Initialize the class at each test."""
    #     pass

    # @classmethod
    # def teardown_method(self):
    #     """Quit the class at each test."""
    #     pass

    def test_init(self):
        with pytest.raises(EmptyError) as e:
            Vector([])
            assert "A vector must have at least one coordinate." in str(e)

        with pytest.raises(TypeError) as e:
            Vector(1.0)
            assert "Type of 'coordinates' must be list[float]." in str(e)

        with pytest.raises(TypeError) as e:
            Vector(["1.0"])
            assert "Type of 'coordinates' must be list[float]." in str(e)

        coordinates: list[float] = [0.0, 1.5, -2.5]
        vector = Vector(coordinates=coordinates)
        assert coordinates == vector.coordinates

        coordinates_set: list[float] = [1.5, -2.5]
        vector.coordinates = coordinates_set
        assert coordinates_set == vector.coordinates

    def test_length(self):
        coordinates: list[float] = [0.0, 1.5, -2.5]
        vector = Vector(coordinates=coordinates)
        assert len(coordinates) == vector.length

    def test_str(self):
        coordinates: list[float] = [0.0, 1.5, -2.5]
        vector = Vector(coordinates=coordinates)
        vector_str = f"[{';\n'.join([str(x) for x in coordinates])}]"
        assert vector_str == str(vector)

    def test_getitem(self):
        coordinates: list[float] = [0.0, 1.5, -2.5]
        vector = Vector(coordinates=coordinates)

        with pytest.raises(TypeError) as e:
            vector["1"]
            assert "The type of 'key' must be int." in str(e)

        with pytest.raises(IndexError) as e:
            vector[len(coordinates)]
            assert f"'key' must be between 0 and {len(coordinates) - 1}" in str(e)

        assert vector[1] == coordinates[1]

    def test_setitem(self):
        coordinates: list[float] = [0.0, 1.5, -2.5]
        vector: Vector = Vector(coordinates=coordinates)

        index = 1
        coordinate: float = 0.5
        coordinates[index] = coordinate

        with pytest.raises(TypeError) as e:
            vector["1"] = coordinate
            assert "The type of 'key' must be int." in str(e)

        with pytest.raises(IndexError) as e:
            vector[len(coordinates)] = coordinate
            assert f"'key' must be between 0 and {len(coordinates) - 1}" in str(e)

        with pytest.raises(TypeError) as e:
            vector[1] = str(coordinate)
            assert "The type of 'coordinate' must be float." in str(e)

        vector[index] = coordinate
        assert vector.coordinates == coordinates

    def test_add(self):
        coordinates1: list[float] = [0.0, 1.5, -2.5]
        vector1: Vector = Vector(coordinates=coordinates1)
        coordinates2: list[float] = [0.0, 1.5, -2.5]
        vector2: Vector = Vector(coordinates=coordinates2)

        assert (vector1 + vector2) == Vector(
            [x + y for x, y in zip(coordinates1, coordinates2)]
        )
