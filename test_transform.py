
from etl.transform import transform_users
import requests


def test_transform_users_success(mocker):
    # Simula a resposta da API
    mock_get = mocker.patch("etl.transform.requests.get")

    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "Ricardo",
        "profile": "Conservador",
        "age": 35,
        "objective": "Preservar patrimônio",
        "news": [],
        "sent_campaigns": []
    }

    mock_get.return_value.raise_for_status.return_value = None

    users = [
        {
            "UserID": 1,
            "Nome": "Ricardo",
            "Perfil": "Conservador"
        }
    ]

    result = transform_users(users, "campanha_teste")

    assert len(result) == 1
    assert result[0]["name"] == "Ricardo"
    assert result[0]["profile"] == "Conservador"
    mock_get.assert_called_once()


def test_transform_users_campaign_already_sent(mocker):
    # Simula cliente que já recebeu a campanha
    mock_get = mocker.patch("etl.transform.requests.get")

    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "Ricardo",
        "profile": "Conservador",
        "age": 35,
        "objective": "Preservar patrimônio",
        "news": ["Mensagem anterior"],
        "sent_campaigns": ["campanha_teste"]
    }

    mock_get.return_value.raise_for_status.return_value = None

    users = [
        {
            "UserID": 1,
            "Nome": "Ricardo",
            "Perfil": "Conservador"
        }
    ]

    result = transform_users(users, "campanha_teste")

    assert len(result) == 0
    mock_get.assert_called_once()


def test_transform_users_api_error(mocker):
    # Simula erro de comunicação com a API
    mock_get = mocker.patch("etl.transform.requests.get")

    mock_get.side_effect = requests.ConnectionError(
        "API indisponível"
    )

    users = [
        {
            "UserID": 1,
            "Nome": "Ricardo",
            "Perfil": "Conservador"
        }
    ]

    try:
        transform_users(users, "campanha_teste")
        assert False, "Era esperado um erro de conexão."
    except requests.ConnectionError:
        assert True
