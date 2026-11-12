
import logging
from pathlib import Path

from etl.extract import extract_users
from etl.transform import transform_users
from etl.ai import generate_messages
from etl.load import load_messages


# Configuração dos logs
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "etl.log"

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
        logger.info("[1/4] Extraindo clientes...")
        users = extract_users()
        logger.info("%s clientes extraídos.", len(users))

        # 2. TRANSFORM
        logger.info("[2/4] Enriquecendo dados...")
        users = transform_users(users)
        logger.info("%s clientes enriquecidos.", len(users))

        # 3. AI
        logger.info("[3/4] Gerando mensagens com IA...")
        messages = generate_messages(users)
        logger.info("%s mensagens geradas.", len(messages))

        # 4. LOAD
        logger.info("[4/4] Gravando mensagens na API...")
        load_messages(messages)

        logger.info("===== PROCESSO ETL FINALIZADO COM SUCESSO =====")

    except Exception:
        logger.exception("ERRO DURANTE A EXECUÇÃO DO PROCESSO ETL")
        raise


if __name__ == "__main__":
    main()

import logging
from pathlib import Path

from etl.extract import extract_users
from etl.transform import transform_users
from etl.ai import generate_messages
from etl.load import load_messages


# Configuração dos logs
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "etl.log"

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
        logger.info("[1/4] Extraindo clientes...")
        users = extract_users()
        logger.info("%s clientes extraídos.", len(users))

        # 2. TRANSFORM
        logger.info("[2/4] Enriquecendo dados...")
        users = transform_users(users)
        logger.info("%s clientes enriquecidos.", len(users))

        # 3. AI
        logger.info("[3/4] Gerando mensagens com IA...")
        messages = generate_messages(users)
        logger.info("%s mensagens geradas.", len(messages))

        # 4. LOAD
        logger.info("[4/4] Gravando mensagens na API...")
        load_result = load_messages(messages)

        if load_result["failed"] > 0:
            logger.warning("ETL finalizado com falhas no carregamento.")
        else:
            logger.info("===== PROCESSO ETL FINALIZADO COM SUCESSO =====")

    except Exception:
        logger.exception("ERRO DURANTE A EXECUÇÃO DO PROCESSO ETL")
        raise


if __name__ == "__main__":
    main()
