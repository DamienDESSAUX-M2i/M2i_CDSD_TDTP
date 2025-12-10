import time

import requests

BASE_URL = "http://quotes.toscrape.com"
ROBOTS_TXT_URL = "/".join([BASE_URL, "robots.txt"])

# Question 1
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
}

response = requests.get(url=BASE_URL, headers=headers)

# Question 2
print("Code status : ", response.status_code)

# Question 3
print("500 premiéres lignes : \n", response.text[:500])

# Question 4
print("Encodage : ", response.encoding)

# Question 5
print("Hearders : ", response.headers)

# Question 6
# response = requests.get(url=ROBOTS_TXT_URL, headers=headers)
# print("robots.txt : \n", response.text)

# Bonus
session = requests.Session()
session.headers.update(headers)
responses = []
for k in range(3):
    response = session.get(BASE_URL)
    responses.append(response)
    time.sleep(2)
session.close()

for k, response in enumerate(responses, start=1):
    print(f"Réponse {k} : ", response.text[:15])
