
import logging
from pathlib import Path

from etl.extract import extract_users
from etl.transform import transform_users
from etl.ai import generate_messages
from etl.load import load_messages
from etl.email import send_messages_by_email


# Configuração dos logs
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "etl.log"

CAMPAIGN_ID = "validacao_final_2026_11_13"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


def main():
    logger.info("===== INICIANDO PROCESSO ETL =====")

    try:
        # 1. EXTRACT
        logger.info("[1/5] Extraindo clientes...")
        users = extract_users()
        logger.info("%s clientes extraídos.", len(users))

        # 2. TRANSFORM
        logger.info("[2/5] Enriquecendo dados...")
        users = transform_users(users, CAMPAIGN_ID)
        logger.info("%s clientes pendentes para a campanha.", len(users))

        # 3. AI
        logger.info("[3/5] Gerando mensagens com IA...")
        messages = generate_messages(users)
        logger.info("%s mensagens geradas.", len(messages))

        # 4. LOAD
        logger.info("[4/5] Gravando mensagens na API...")
        load_result = load_messages(messages, CAMPAIGN_ID)

        # 5. EMAIL
        logger.info("[5/5] Enviando mensagens por e-mail...")
        email_result = send_messages_by_email(
            load_result["to_email"]
        )

        logger.info(
            "Resumo dos e-mails: %s enviados, %s ignorados, %s com falha.",
            email_result["sent"],
            email_result["skipped"],
            email_result["failed"]
        )

        # RESULTADO FINAL
        if load_result["failed"] > 0 or email_result["failed"] > 0:
            logger.warning(
                "===== PROCESSO ETL FINALIZADO COM FALHAS ====="
            )
        else:
            logger.info(
                "===== PROCESSO ETL FINALIZADO COM SUCESSO ====="
            )

    except Exception:
        logger.exception("ERRO DURANTE A EXECUÇÃO DO PROCESSO ETL")
        raise


if __name__ == "__main__":
    main()
