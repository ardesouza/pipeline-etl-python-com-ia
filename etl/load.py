
import logging
import requests

API_URL = "http://127.0.0.1:8000"

logger = logging.getLogger(__name__)


def load_messages(messages):
    successful = 0
    skipped = 0
    failed = 0

    for item in messages:
        user_id = item["user_id"]
        name = item["name"]
        message = item["message"]

        try:
            # Consulta o cadastro do cliente
            response = requests.get(
                f"{API_URL}/users/{user_id}",
                timeout=10
            )
            response.raise_for_status()

            user = response.json()

            # Evita mensagens exatamente iguais
            if message in user.get("news", []):
                logger.info(
                    "Mensagem já existe para %s. Ignorando.",
                    name
                )
                skipped += 1
                continue

            # Grava a mensagem na API
            response = requests.put(
                f"{API_URL}/users/{user_id}/news",
                json={"message": message},
                timeout=10
            )
            response.raise_for_status()

            logger.info(
                "Mensagem gravada para %s com sucesso!",
                name
            )
            successful += 1

        except requests.RequestException:
            logger.exception(
                "Erro de comunicação com a API para o cliente %s (ID %s).",
                name,
                user_id
            )
            failed += 1

        except (KeyError, TypeError, ValueError):
            logger.exception(
                "Erro nos dados do cliente %s (ID %s).",
                name,
                user_id
            )
            failed += 1

    logger.info(
        "Resumo do carregamento: %s gravadas, %s ignoradas, %s com falha.",
        successful,
        skipped,
        failed
    )

    return {
        "successful": successful,
        "skipped": skipped,
        "failed": failed
    }
