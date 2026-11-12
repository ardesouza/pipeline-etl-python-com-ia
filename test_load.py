import requests

from etl.load import load_messages


def test_load_messages_success(mocker):
    # Simula a consulta do cliente
    mock_get = mocker.patch("etl.load.requests.get")
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "Ricardo",
        "news": []
    }
    mock_get.return_value.raise_for_status.return_value = None

    # Simula a gravação da mensagem
    mock_put = mocker.patch("etl.load.requests.put")
    mock_put.return_value.raise_for_status.return_value = None

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "message": "Mensagem de teste."
        }
    ]

    result = load_messages(messages)

    assert result["successful"] == 1
    assert result["skipped"] == 0
    assert result["failed"] == 0

    mock_put.assert_called_once()

def test_load_messages_duplicate(mocker):
    # Simula cliente que já possui a mensagem
    mock_get = mocker.patch("etl.load.requests.get")
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "Ricardo",
        "news": ["Mensagem já cadastrada."]
    }
    mock_get.return_value.raise_for_status.return_value = None

    mock_put = mocker.patch("etl.load.requests.put")

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "message": "Mensagem já cadastrada."
        }
    ]

    result = load_messages(messages)

    assert result["successful"] == 0
    assert result["skipped"] == 1
    assert result["failed"] == 0

    # Confirma que não houve nova gravação
    mock_put.assert_not_called()


def test_load_messages_api_error(mocker):
    # Simula falha de comunicação com a API
    mock_get = mocker.patch("etl.load.requests.get")
    mock_get.side_effect = requests.ConnectionError(
        "API indisponível"
    )

    messages = [
        {
            "user_id": 1,
            "name": "Ricardo",
            "message": "Mensagem de teste."
        }
    ]

    result = load_messages(messages)

    assert result["successful"] == 0
    assert result["skipped"] == 0
    assert result["failed"] == 1