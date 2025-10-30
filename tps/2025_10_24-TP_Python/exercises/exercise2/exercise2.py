def main() -> None:
    print("=== Tables de multiplication ===")
    for i in range(1, 11):
        print(f"=== Table de {i} ===")
        for j in range(0, 11):
            print(f"{i} \\times {j} = {i * j}")
        print("")


if __name__ == "__main__":
    main()
