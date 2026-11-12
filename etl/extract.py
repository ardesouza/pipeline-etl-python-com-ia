
import pandas as pd
from pathlib import Path

# Localização do arquivo CSV
BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "SDW2023.csv"


def extract_users():
    # Verifica se o arquivo existe
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CSV_PATH}")

    # Lê os dados do CSV
    df = pd.read_csv(CSV_PATH)

    # Valida as colunas necessárias
    required_columns = {"UserID", "Nome", "Perfil"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas ausentes no CSV: {missing_columns}"
        )

    # Padroniza o ID como número inteiro
    df["UserID"] = pd.to_numeric(
        df["UserID"], errors="raise"
    ).astype(int)

    # Converte os registros para uma lista de dicionários
    users = df.to_dict(orient="records")

    return users
