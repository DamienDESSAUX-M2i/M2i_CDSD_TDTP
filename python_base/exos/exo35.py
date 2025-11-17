def compute(a: float, b: float) -> tuple[float]:
    return a+b, a-b, a/b, a*b

def enter_number(msg: str, msg_error: str) -> float:
    while True:
        user_input = input(msg)
        try:
            nb = float(user_input)
            return nb
        except ValueError:
            print(msg_error)
        finally:
            pass

def main():
    msg1: str = "Enter un permier nombre : "
    msg2: str = "Enter un second nombre : "
    msg_error: str = "Saisie non valide"
    nb1: float = enter_number(msg=msg1, msg_error=msg_error)
    nb2: float = enter_number(msg=msg2, msg_error=msg_error)
    s, d, q, p = compute(a=nb1, b=nb2)
    print(f"La somme de {nb1} et {nb2} est {s}.")
    print(f"La différence de {nb1} et {nb2} est {d}.")
    print(f"Le quotient de {nb1} et {nb2} est {q}.")
    print(f"Le produit de {nb1} et {nb2} est {p}.")

if __name__ == "__main__":
    main()