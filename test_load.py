
import requests

from etl.load import load_messages


def test_load_messages_success(mocker):
    # Simula gravação bem-sucedida na API
    mock_put = mocker.patch("etl.load.requests.put")

    mock_put.return_value.json.return_value = {
        "message": "Mensagem cadastrada com sucesso.",
        "already_sent": False,
        "user": {
            "id": 1,
            "name": "Ricardo",
            "news": ["Mensagem de teste."]
        }
    }

    mock_put.return_value.raise_for_status.return_value = None

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "email": "ricardo@teste.com",
            "message": "Mensagem de teste."
        }
    ]

    result = load_messages(messages, "campanha_teste")

    assert result["successful"] == 1
    assert result["skipped"] == 0
    assert result["failed"] == 0
    assert len(result["to_email"]) == 1

    mock_put.assert_called_once()


def test_load_messages_duplicate(mocker):
    # Simula campanha já processada na API
    mock_put = mocker.patch("etl.load.requests.put")

    mock_put.return_value.json.return_value = {
        "message": "Esta campanha já foi processada para este cliente.",
        "already_sent": True,
        "user": {
            "id": 1,
            "name": "Ricardo",
            "news": ["Mensagem já cadastrada."]
        }
    }

    mock_put.return_value.raise_for_status.return_value = None

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "email": "ricardo@teste.com",
            "message": "Mensagem já cadastrada."
        }
    ]

    result = load_messages(messages, "campanha_teste")

    assert result["successful"] == 0
    assert result["skipped"] == 1
    assert result["failed"] == 0
    assert len(result["to_email"]) == 0

    mock_put.assert_called_once()


def test_load_messages_api_error(mocker):
    # Simula falha de comunicação com a API
    mock_put = mocker.patch("etl.load.requests.put")

    mock_put.side_effect = requests.ConnectionError(
        "API indisponível"
    )

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "email": "ricardo@teste.com",
            "message": "Mensagem de teste."
        }
    ]

    result = load_messages(messages, "campanha_teste")

    assert result["successful"] == 0
    assert result["skipped"] == 0
    assert result["failed"] == 1
    assert len(result["to_email"]) == 0

    mock_put.assert_called_once()
