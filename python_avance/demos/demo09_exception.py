class MyException(Exception):
    def __init__(self, msg, *args):
        self.msg = msg

def main1():
    try:
        n = int(input("Saisir un entier naturel :"))
        if n < 0:
            raise MyException("L'entier est négatif", n)
    except ValueError:
        print("Saisie invalide.")
    except Exception as e:
        print("Autre exception.")
        print(e)
    else:
        print('Saisie valide.')
    finally:
        print("Fin du test.")

main1()