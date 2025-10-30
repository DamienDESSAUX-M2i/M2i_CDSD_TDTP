from math import ceil, sqrt


def user_input(msg: str, msg_error: str) -> int:
    """Allow a user to enter an natural integer.

    Args:
        msg (str): Message to display.
        msg_error (str): Error message to display.

    Returns:
        int: The value entered by the user.
    """
    nb: int = 0
    while True:
        user_input: str = input(msg)
        try:
            nb: int = int(user_input)
            if nb >= 0:
                return nb
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)


# This function needs to be improved
# Complexity : O(n**2)
def decompose_integer(n: int) -> list[tuple[int]]:
    """Decompose a natural number into the sum of consecutive integers.

    Args:
        n (int): A natural number.

    Returns:
        list[tuple[int]]: The list of possible decompositions.
    """
    decompositions: list[tuple[int]] = []
    for p in range(1, ceil(n / 2)):
        for q in range(p + 1, ceil(n / 2) + 1):
            if sum(range(p, q + 1)) == n:
                decompositions.append((p, q))
    return decompositions


# Complexity : O(sqrt(2*n))
## Let a in N* and k in N* such that
## n = a + ... + (a + k - 1) = (k * (2a + k - 1)) / 2
## So 2 * n = k * (2a + k - 1)
## We are looking for k a divisor of 2*n
## If k is a divisor of 2*n then (2a + k - 1) in N*
## Let l in N* such that l = 2a + k - 1
## So 2*a = l - k + 1
## If (l - k + 1) is divided by 2
## then a = (l - k + 1) // 2 in Z
## Finally if a > 0 the decomposition is valid.
def decompose_integer_optimized(n: int) -> list[tuple[int]]:
    """Decompose a natural number into the sum of consecutive integers.

    Args:
        n (int): A natural number.

    Returns:
        list[tuple[int]]: The list of possible decompositions.
    """
    decompositions: list[tuple[int]] = []
    for k in range(1, ceil(sqrt(2 * n))):
        if (2 * n) % k == 0:
            l: float = (2 * n) // k
            if (l - k + 1) % 2 == 0: # 2a
                a = (l - k + 1) // 2
                if a > 0:
                    decompositions.append((a, a + k - 1))
    return decompositions


def display_decompositions(n: int, decompositions: list[tuple[int]]) -> None:
    """Display all decompositions of a natural number in sum of consecutive integers.

    Args:
        n (int): A natural number to decompose.
        decompositions (list[tuple[int]]): The list of possible decompositions.
    """
    print(f"=== Décomposition du nombre {n} en somme d'entiers consécutifs ===")
    if decompositions:
        for decomposition in decompositions:
            p, q = decomposition
            print(f"{n} = {' + '.join([str(x) for x in range(p, q + 1)])}")
    else:
        print(f"{n} = {n}")


def main() -> None:
    """Main function."""
    msg: str = "Saisir un entier naturel à décomposer en somme d'entiers consécutifs : "
    msg_error: str = "Errreur de saisie. Veuillez recommencer."
    n: int = user_input(msg=msg, msg_error=msg_error)
    decompositions: list[tuple[int]] = decompose_integer_optimized(n=n)
    display_decompositions(n=n, decompositions=decompositions)


if __name__ == "__main__":
    main()
