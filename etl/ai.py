
import os
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")

# Inicializa o cliente Groq
client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


def generate_message(user):
    prompt = f"""
    Crie uma mensagem educativa e personalizada sobre educação
    financeira para o cliente abaixo.

    Nome: {user['name']}
    Perfil de investidor: {user['profile']}
    Idade: {user['age']}
    Objetivo financeiro: {user['objective']}

    Orientações:
    - Utilize o primeiro nome do cliente.
    - Considere seu perfil de investidor.
    - Considere seu objetivo financeiro.
    - Escreva de forma simples, natural e profissional.
    - Produza uma mensagem entre 50 e 90 palavras.
    - Não recomende ativos específicos nem prometa rentabilidade.
    - Não apresente a mensagem como recomendação individual
      de investimento.
    - Não indique percentuais de renda ou valores para investir.
    - Não recomende produtos, fundos ou classes específicas
      de investimentos.
    - Priorize conceitos gerais de educação financeira,
      planejamento, organização e controle financeiro.
    - Entregue somente o texto da mensagem.
    - Não indique prazos, percentuais ou valores específicos
      para poupança ou reserva financeira.
    - Não recomende aplicações financeiras, investimentos
      ou estratégias específicas.
    - Não utilize expressões que indiquem uma decisão
      individual de investimento para o cliente.
    - Limite-se a orientações educativas e gerais sobre
      organização e planejamento financeiro.
    """
    

    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente especializado em "
                    "educação financeira."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=800,
        reasoning_effort="low",
        include_reasoning=False
    )

    message = response.choices[0].message.content

    if not message or not message.strip():
        raise ValueError(
            "A IA retornou uma resposta vazia. "
            "Verifique o limite de tokens e a resposta da API."
        )

    return message.strip()

def generate_messages(users):
    messages = []

    for user in users:
        print(f"Gerando mensagem para {user['name']}...")

        message = generate_message(user)

        messages.append({
            "user_id": user["id"],
            "name": user["name"],
            "email": user.get("email"),
            "message": message
        })

    return messages

