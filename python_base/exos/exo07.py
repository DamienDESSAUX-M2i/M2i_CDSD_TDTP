def print_calculus(a:int, b:int) -> None:
    """Print a² + b²

    Args:
        a (int): a
        b (int): b
    """
    print(f"a² + b² = {a**2 + b**2}")

def main() -> None:
    """Main function
    """
    a = 2
    b = 3
    print_calculus(a=a,b=b)


if __name__ == "__main__":
    main()