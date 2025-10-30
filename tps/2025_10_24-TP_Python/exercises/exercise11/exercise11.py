from typing import TypedDict
from pathlib import Path
import csv


class Msgs(TypedDict):
    """Format of a dictionary containing the messages to be displayed.

    Keys:
        msg_main (str): Message when starting the programme.
        msg_display (str): Message when displaying a secret.
        msg_add (str): Message when adding a secret.
        msg_modify (str): Message when modifying a secret.
        msg_remove (str): Message when removing a secret.
        msg_error (str): Error message.
        msg_nb_secrets (str) : Number of recorded secrets.
    """

    msg_main: str
    msg_display: str
    msg_add: str
    msg_modify: str
    msg_remove: str
    msg_error: str
    msg_nb_secrets: str


def user_input_index(my_list: list, msg: str, msg_error: str) -> int:
    """Allow a user to give a natural number between 1 and the the length of the list 'my_list'

    Args:
        my_list (list): A list.
        msg (str): The message to display to the user.
        msg_error (str): The error message to display to the user.

    Raises:
        IndexError: The list 'my_list' can not be empty.

    Returns:
        int: _description_
    """
    if not my_list:
        raise IndexError("'my_list' is empty.")
    while True:
        user_input: str = input(msg)
        try:
            index_secret: int = int(user_input)
            if 1 <= index_secret < (len(my_list) + 1):
                return index_secret - 1
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)


def display_secret(secrets: list[str], index_secret: int, msg: str) -> None:
    """Display a secret.

    Args:
        secrets (list[str]): The secrets of a user.
        index_secret (int): The index of the secret to be displayed.
        msg (str): The message to display to a user.
    """
    print(f"{msg}{index_secret + 1} : {secrets[index_secret]}\n")


def write_secret(secrets: list[str], msg: str) -> None:
    """Allow the user ti write a secret, then add the secret to the list 'secrets'.

    Args:
        secrets (list[str]): The secrets of a user.
        msg (str): The message to display to the user.
    """
    secrets.append(input(msg))


def modify_secret(secrets: list[str], index_secret: int, msg: str) -> None:
    """Allow a user to write a secret, then insert the secret in the list 'secrets' to a given index.

    Args:
        secrets (list[str]): The secrets of the user.
        index_secret (int): The index of the secret to be modified.
        msg (str): The message to display to the user.
    """
    secrets[index_secret] = input(msg)


def remove_secret(secrets: list[str], index_secret: int) -> None:
    """Remove a secret.

    Args:
        secrets (list[str]): The secrets of the user.
        index_secret (int): The index of the secret to remove.
    """
    secrets.pop(index_secret)


def menu_main(file_path: Path, secrets: list[str], msgs: Msgs) -> None:
    """Allow a user to write, read, modify, and delete secrets.

    Args:
        file_path (Path) : Path of a csv file.
        secrets (list[str]): The list of secrets of the user..
        msgs (Msgs): Dictionary containing messages to display.
    """
    while True:
        user_input: str = input(msgs["msg_main"])
        match user_input:
            case "1":  # Display
                print(f"{msgs['msg_nb_secrets']}{len(secrets)}")
                if secrets:
                    index_secret: int = user_input_index(
                        my_list=secrets,
                        msg=msgs["msg_display"],
                        msg_error=msgs["msg_error"],
                    )
                    display_secret(
                        secrets=secrets,
                        index_secret=index_secret,
                        msg=msgs["msg_nb_secret"],
                    )
            case "2":  # Add
                write_secret(secrets=secrets, msg=msgs["msg_add"])
            case "3":  # Modify
                print(f"{msgs['msg_nb_secrets']}{len(secrets)}")
                if secrets:
                    index_secret: int = user_input_index(
                        my_list=secrets,
                        msg=msgs["msg_modify"],
                        msg_error=msgs["msg_error"],
                    )
                    modify_secret(
                        secrets=secrets, index_secret=index_secret, msg=msgs["msg_add"]
                    )
            case "4":  # Remove
                print(f"{msgs['msg_nb_secrets']}{len(secrets)}")
                if secrets:
                    index_secret: int = user_input_index(
                        my_list=secrets,
                        msg=msgs["msg_remove"],
                        msg_error=msgs["msg_error"],
                    )
                    remove_secret(secrets=secrets, index_secret=index_secret)
            case "5":  # Exit
                write_secrets(file_path=file_path, secrets=secrets)
                exit()
            case _:
                print(msgs["msg_error"])


def load_secrets(file_path: Path) -> list[str]:
    """Load a csv file containing secrets of the user.

    Args:
        file_path (Path): Path of the csv file.

    Returns:
        list[str]: The secrets of the user.
    """
    secrets: list[str] = []
    with open(file_path, "rt", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["secret"]
        csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames, delimiter="|")
        for row in csv_reader:
            secrets.append(row["secret"])
    secrets.pop(0)  # Remove header
    return secrets


def write_secrets(file_path: Path, secrets: list[str]) -> None:
    """Write the secrets of the user in a csv file.

    Args:
        file_path (Path): The path of the csv file.
        secrets (list[str]): The secrets of the user.
    """
    with open(file_path, "wt", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["secret"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
        csv_writer.writeheader()
        for k in range(len(secrets)):
            csv_writer.writerow({"secret": secrets[k]})


def main() -> None:
    """Main function"""

    secrets: list[str] = []
    file_path: Path = Path("./exercises/exercise11/secrets.csv")
    if Path.exists(file_path):
        secrets = load_secrets(file_path=file_path)

    msgs: Msgs = {}
    msgs["msg_add"] = "Ecrivez votre secret puis appuyez sur entrer.\n=> "
    msgs["msg_display"] = "Numéro du secret que vous voulez afficher : "
    msgs["msg_main"] = (
        "=== Menu ===\n[1] Afficher un secret\n[2] Ajouter un secret\n[3] Modifier un secret\n[4] Supprimer un secret\n[5] Quitter et sauvegarder\n=> "
    )
    msgs["msg_modify"] = "Numéro du secret que vous voulez modifier : "
    msgs["msg_remove"] = "Numéro du secret que vous voulez supprimer : "
    msgs["msg_nb_secrets"] = "Nombre de secrets enregistrés : "
    msgs["msg_nb_secret"] = "Secret no"
    msgs["msg_error"] = "Errreur de saisie. Veuillez recommencer."

    menu_main(file_path=file_path, secrets=secrets, msgs=msgs)


if __name__ == "__main__":
    main()
