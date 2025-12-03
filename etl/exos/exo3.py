from collections import Counter
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# Question 1
endpoint = "users"
response = requests.get(url="/".join([BASE_URL, endpoint]))
entries = response.json()

# Question 2
for entry in entries:
    print(f"nom : {entry['name']}, email : {entry['email']}")

# Question 3
endpoint = "posts"
params = {"userId": 1}
response = requests.get(url="/".join([BASE_URL, endpoint]), params=params)

# Question 4
endpoint = "posts"
response = requests.get(url="/".join([BASE_URL, endpoint]))
entries = response.json()
userIds = [entry["userId"] for entry in entries]
for user_id, nb_occurrences in Counter(userIds).items():
    print(f"userId : {user_id} - nombre d'occurrences : {nb_occurrences}")

# Question 5
endpoint = "comments"
params = {"postId": 1}
response = requests.get(url="/".join([BASE_URL, endpoint]), params=params)
entries = response.json()
for entry in entries:
    print(entry["body"])

# Question 6
endpoint = "posts"
params = {"_limit": 10}
response = requests.get(url="/".join([BASE_URL, endpoint]), params=params)
entries_posts = response.json()

data = {"post_id": [], "post_title": [], "nombre_commentaires": []}
for entry in entries_posts:
    id: int = entry["id"]
    title: str = entry["title"]
    data["post_id"].append(id)
    data["post_title"].append(title)

    endpoint = f"posts/{id}/comments"
    response = requests.get(url="/".join([BASE_URL, endpoint]))
    entries_comments = response.json()
    data["nombre_commentaires"].append(len(entries_comments))

df = pd.DataFrame(data)

dir_path: Path = Path(__file__).parent.resolve()
file_csv_path: Path = dir_path.joinpath("exo3.csv")
df.to_csv(file_csv_path, index=False)

# Bonus
endpoint = "todos"
response = requests.get(url="/".join([BASE_URL, endpoint]))
entries_todos = response.json()

data_todos_completed = {"id": [], "userId": [], "title": []}
data_todos_not_completed = {"id": [], "userId": [], "title": []}
for entry in entries_todos:
    id: int = entry["id"]
    user_id: int = entry["userId"]
    title: str = entry["title"]
    completed: bool = entry["completed"]
    if completed:
        data_todos_completed["id"].append(id)
        data_todos_completed["userId"].append(user_id)
        data_todos_completed["title"].append(title)
    data_todos_not_completed["id"].append(id)
    data_todos_not_completed["userId"].append(user_id)
    data_todos_not_completed["title"].append(title)

df_completed = pd.DataFrame(data_todos_completed)
df_not_completed = pd.DataFrame(data_todos_not_completed)

file_xlsx_path: Path = dir_path.joinpath("exo3.xlsx")
with pd.ExcelWriter(file_xlsx_path) as writer:
    df_completed.to_excel(writer, index=False, sheet_name="completed")
    df_not_completed.to_excel(writer, index=False, sheet_name="not completed")
