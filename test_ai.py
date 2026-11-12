
from types import SimpleNamespace

from etl.ai import generate_message, generate_messages


def test_generate_message_success(mocker):
    # Simula a resposta da Groq
    mock_create = mocker.patch(
        "etl.ai.client.chat.completions.create"
    )

    mock_create.return_value = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Mensagem educativa de teste."
                )
            )
        ]
    )

    user = {
        "id": 1,
        "name": "Ricardo",
        "profile": "Conservador",
        "age": 35,
        "objective": "Preservar patrimônio",
        "news": []
    }

    result = generate_message(user)

    assert result == "Mensagem educativa de teste."
    mock_create.assert_called_once()


def test_generate_message_empty_response(mocker):
    # Simula uma resposta vazia da IA
    mock_create = mocker.patch(
        "etl.ai.client.chat.completions.create"
    )

    mock_create.return_value = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="")
            )
        ]
    )

    user = {
        "id": 1,
        "name": "Ricardo",
        "profile": "Conservador",
        "age": 35,
        "objective": "Preservar patrimônio",
        "news": []
    }

    try:
        generate_message(user)
        assert False, "Era esperado um erro de resposta vazia."
    except ValueError as error:
        assert "resposta vazia" in str(error)


def test_generate_messages_multiple_users(mocker):
    # Simula a geração das mensagens sem chamar a Groq
    mock_generate = mocker.patch(
        "etl.ai.generate_message",
        return_value="Mensagem educativa de teste."
    )

    users = [
        {
            "id": 1,
            "name": "Ricardo",
            "profile": "Conservador",
            "age": 35,
            "objective": "Preservar patrimônio"
        },
        {
            "id": 2,
            "name": "Mariana",
            "profile": "Moderado",
            "age": 29,
            "objective": "Construir patrimônio"
        }
    ]

    result = generate_messages(users)

    assert len(result) == 2
    assert result[0]["user_id"] == 1
    assert result[1]["user_id"] == 2
    assert all(
        item["message"] == "Mensagem educativa de teste."
        for item in result
    )

    assert mock_generate.call_count == 2
