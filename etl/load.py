
import logging
import requests

API_URL = "http://127.0.0.1:8000"

logger = logging.getLogger(__name__)



def load_messages(messages, campaign_id):
    successful = 0
    skipped = 0
    failed = 0
    to_email = []

    for item in messages:
        user_id = item["user_id"]
        name = item["name"]
        message = item["message"]

        try:
            response = requests.put(
                f"{API_URL}/users/{user_id}/news",
                json={
                    "message": message,
                    "campaign_id": campaign_id
                },
                timeout=10
            )

            response.raise_for_status()
            result = response.json()

            if result.get("already_sent"):
                logger.info(
                    "Campanha %s já processada para %s. Ignorando.",
                    campaign_id,
                    name
                )
                skipped += 1
                continue

            logger.info(
                "Mensagem gravada para %s com sucesso!",
                name
            )
            to_email.append(item)
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
        "failed": failed,
        "to_email": to_email
    }
