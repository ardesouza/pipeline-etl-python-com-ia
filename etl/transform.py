
import requests

API_URL = "http://127.0.0.1:8000"


def transform_users(users):
    enriched_users = []

    for user in users:
        user_id = user["UserID"]

        # Consulta o cliente na API
        response = requests.get(
            f"{API_URL}/users/{user_id}",
            timeout=10
        )

        response.raise_for_status()

        # Recupera o cadastro completo
        api_user = response.json()

        enriched_users.append(api_user)

    return enriched_users
