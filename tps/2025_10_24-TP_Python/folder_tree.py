import os

if not os.path.exists("./exercises"):
    exs = []
    with open("exercices_bonus.md", "rt", encoding="utf-8", newline="") as exs_bonus:
        cpt = 0
        ex = ""
        for line in exs_bonus:
            if "Exercice " in line:
                if cpt > 0:
                    exs.append(ex)
                    ex = ""
                cpt += 1
            ex += line
        exs.append(ex)

    os.mkdir("./exercises")
    with open("./exercises/__ini__.py", "wt", encoding="utf-8") as py_file:
        pass

    for k in range(1, 15):
        os.mkdir(f"./exercises/exercise{k}")
        with open(
            f"./exercises/exercise{k}/exercise{k}.md", "wt", encoding="utf-8"
        ) as md_file:
            for line in exs[k - 1]:
                md_file.write(line)
        with open(
            f"./exercises/exercise{k}/exercise{k}.py", "wt", encoding="utf-8"
        ) as py_file:
            py_file.write("def main() -> None:")
            py_file.write("\tpass")
            py_file.write("")
            py_file.write("")
            py_file.write('if __name__ == "__main__":')
            py_file.write("\tmain()")
            py_file.write("")
        with open(
            f"./exercises/exercise{k}/__ini__.py", "wt", encoding="utf-8"
        ) as py_file:
            pass
else:
    print("The 'exercises' folder already exists")
