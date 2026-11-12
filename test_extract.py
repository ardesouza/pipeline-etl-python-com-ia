
from etl.extract import extract_users


def test_extract_users_success(tmp_path, monkeypatch):
    # Cria um CSV temporário para o teste
    csv_file = tmp_path / "clientes.csv"

    csv_file.write_text(
        "UserID,Nome,Perfil\n"
        "1,Ricardo,Conservador\n"
        "2,Mariana,Moderado\n",
        encoding="utf-8"
    )

    # Direciona a extração para o CSV temporário
    monkeypatch.setattr(
        "etl.extract.CSV_PATH",
        csv_file
    )

    users = extract_users()

    assert len(users) == 2
    assert users[0]["UserID"] == 1
    assert users[0]["Nome"] == "Ricardo"
    assert users[1]["Perfil"] == "Moderado"


def test_extract_users_file_not_found(monkeypatch):
    from pathlib import Path

    monkeypatch.setattr(
        "etl.extract.CSV_PATH",
        Path("arquivo_inexistente.csv")
    )

    try:
        extract_users()
        assert False, "Era esperado um erro de arquivo não encontrado."
    except FileNotFoundError:
        assert True


def test_extract_users_missing_columns(tmp_path, monkeypatch):
    csv_file = tmp_path / "clientes_invalidos.csv"

    csv_file.write_text(
        "UserID,Nome\n"
        "1,Ricardo\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "etl.extract.CSV_PATH",
        csv_file
    )

    try:
        extract_users()
        assert False, "Era esperado um erro de coluna ausente."
    except ValueError as error:
        assert "Colunas ausentes" in str(error)
