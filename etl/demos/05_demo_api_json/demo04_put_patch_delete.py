import requests

base_url = 'https://jsonplaceholder.typicode.com/posts/1'

# PUT : remplace ENTIEREMENT la ressource

updated_post = {
    'id': 1,
    'title': 'Titre mis à jour',
    'body': 'Nouveau contenu',
    'userId': 1
}

response = requests.put(base_url, json=updated_post)
print("PUT :", response.json())

# PATCH : mise à jour PARTIELLE

partial_update = {
    'title': 'Juste le titre change'
}

response = requests.patch(base_url, json=partial_update)
print("PATCH :", response.json())

# DELETE : suppression

response = requests.delete(base_url)
print("DELETE - statut :", response.status_code)  # 200 ou 204


