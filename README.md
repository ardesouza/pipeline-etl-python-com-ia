# Pipeline ETL com Python e Inteligência Artificial Generativa

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)
![Groq](https://img.shields.io/badge/IA-Groq-orange)
![Pytest](https://img.shields.io/badge/Testes-Pytest-green?logo=pytest)
![Status](https://img.shields.io/badge/Status-Concluído-success)

## Sobre o projeto

Este projeto demonstra a construção de um pipeline ETL (Extract, Transform, Load) utilizando Python, integração de APIs, Inteligência Artificial Generativa e automação de envio de e-mails.

A proposta consiste em simular um processo de enriquecimento de dados de clientes, utilizando informações armazenadas em um arquivo CSV, consultando uma API local para recuperar dados complementares, gerando mensagens educativas personalizadas com auxílio de Inteligência Artificial, armazenando os resultados por meio de uma API e enviando as mensagens por e-mail.

O projeto foi desenvolvido com dados fictícios, sem utilização de informações reais de clientes ou integração com sistemas bancários.

A implementação busca demonstrar, na prática, conceitos de engenharia de dados, automação de processos, integração entre sistemas, tratamento de erros, controle de campanhas e testes automatizados.

## Objetivos

Desenvolver um pipeline ETL utilizando Python.

Realizar extração e validação de dados estruturados.

Integrar aplicações por meio de APIs REST.

Enriquecer informações a partir de uma fonte externa ao CSV.

Utilizar Inteligência Artificial Generativa para produzir conteúdo personalizado.

Implementar mecanismos de tratamento de erros e prevenção de duplicidades.

Controlar o histórico de campanhas enviadas para cada cliente.

Automatizar o envio de mensagens por e-mail utilizando Gmail.

Registrar a execução do processo por meio de logs.

Desenvolver testes automatizados para validar as etapas do pipeline.

Arquitetura do projeto

O pipeline está dividido em cinco etapas principais:

              ARQUIVO CSV
                   |
                   v
          1. EXTRACT (Extração)
                   |
                   v
             DADOS INICIAIS
                   |
                   v
        2. TRANSFORM (Transformação)
                   |
                   v
             API FASTAPI
          Enriquecimento dos dados
          Controle de campanhas
                   |
                   v
            DADOS COMPLETOS
                   |
                   v
          3. INTELIGÊNCIA ARTIFICIAL
                   |
                   v
              GROQ API
          Geração de mensagens
                   |
                   v
             MENSAGENS GERADAS
                   |
                   v
             4. LOAD (Carga)
                   |
                   v
              API FASTAPI
                   |
                   v
           USERS.JSON ATUALIZADO
                   |
                   v
             5. ENVIO DE E-MAIL
                   |
                   v
              GMAIL SMTP
                   |
                   v
           CLIENTES NOTIFICADOS

Funcionamento do pipeline

1. Extract — Extração

A primeira etapa realiza a leitura dos dados de clientes armazenados em um arquivo CSV.

Arquivo: data/SDW2023.csv

Os dados de origem contêm informações como:

Identificador do cliente.

Nome.

Perfil financeiro.

O módulo utiliza a biblioteca Pandas para realizar a leitura e conversão dos registros em uma estrutura de dados manipulável pelo Python.

Também são realizadas validações para verificar:

Existência do arquivo.

Presença das colunas obrigatórias.

Integridade do identificador numérico dos clientes.

Arquivo responsável: etl/extract.py

2. Transform — Transformação e enriquecimento

Nesta etapa, os dados extraídos são utilizados para consultar uma API REST desenvolvida com FastAPI.

A API disponibiliza informações complementares dos clientes, como:

Idade.

Objetivo financeiro.

Perfil.

Histórico de mensagens.

Histórico de campanhas já processadas.

O enriquecimento acontece por meio de requisições HTTP, utilizando o identificador de cada cliente para localizar seu cadastro.

Também é implementado um mecanismo de controle de campanhas. Antes de encaminhar os clientes para a geração de mensagens, o processo verifica se a campanha atual já foi enviada.

Clientes que já receberam a campanha são ignorados, evitando chamadas desnecessárias à Inteligência Artificial e o processamento duplicado.

Arquivo responsável: etl/transform.py

3. Inteligência Artificial — Geração de mensagens

Após o enriquecimento, os dados são encaminhados para a API da Groq, responsável pela geração de conteúdo utilizando um modelo de linguagem.

Modelo utilizado: openai/gpt-oss-20b.

Cada cliente recebe uma mensagem educativa gerada considerando informações como nome, perfil e objetivo financeiro.

O prompt possui orientações para produzir textos:

Personalizados de acordo com os dados disponíveis.

Simples, naturais e profissionais.

Voltados à educação e organização financeira.

Sem recomendações específicas de investimentos.

Sem promessas de rentabilidade ou indicação de produtos financeiros.

A chave de autenticação da API é armazenada em uma variável de ambiente, utilizando o arquivo .env.

Arquivo responsável: etl/ai.py

4. Load — Carregamento

Nesta etapa, as mensagens geradas são encaminhadas para a API FastAPI, que realiza a atualização do cadastro de cada cliente.

O processo utiliza um identificador de campanha (campaign_id) para controlar o histórico de mensagens enviadas.

Antes da gravação, a API verifica se aquela campanha já foi processada para o cliente.

Caso a campanha já esteja registrada, a operação é ignorada. Caso contrário, a mensagem é armazenada e o identificador da campanha é adicionado ao histórico do cliente.

Esse mecanismo garante maior controle sobre a execução e evita o reprocessamento de campanhas já realizadas.

O módulo também possui tratamento de erros para:

Problemas de comunicação com a API.

Falhas durante a consulta dos clientes.

Inconsistências nos dados.

Falhas durante o carregamento.

Ao final, é apresentado um resumo contendo:

Quantidade de mensagens gravadas.

Quantidade de mensagens ignoradas.

Quantidade de operações com falha.

Arquivo responsável: etl/load.py

5. Envio de e-mails — Comunicação com os clientes

Após o carregamento das mensagens na API, o pipeline realiza automaticamente o envio dos conteúdos por e-mail.

A integração utiliza o servidor SMTP do Gmail, com autenticação por credenciais armazenadas em variáveis de ambiente.

O processo considera:

Envio da mensagem personalizada para o endereço cadastrado.

Utilização do nome do cliente e do conteúdo gerado pela IA.

Identificação de clientes sem endereço de e-mail cadastrado.

Registro dos envios realizados.

Tratamento de falhas durante a comunicação com o servidor SMTP.

Clientes sem e-mail cadastrado são ignorados, sem interromper o processamento dos demais.

Ao final, o sistema apresenta um resumo contendo:

Quantidade de e-mails enviados.

Quantidade de envios ignorados.

Quantidade de falhas.

Arquivo responsável: etl/email.py

API REST com FastAPI

O projeto possui uma API local responsável por disponibilizar os cadastros dos clientes e receber as mensagens geradas pelo pipeline.

A persistência dos dados é realizada em um arquivo JSON (api/users.json).

Além das informações cadastrais e do histórico de mensagens, a API mantém o histórico de campanhas processadas para cada cliente, permitindo controlar a duplicidade de envios.

Endpoints disponíveis

Método

Endpoint

Descrição

GET

/

Verifica o funcionamento da API

GET

/users

Lista todos os clientes

GET

/users/{user_id}

Consulta um cliente específico

PUT

/users/{user_id}/news

Adiciona uma mensagem e registra a campanha

O endpoint de atualização recebe o conteúdo da mensagem e o identificador da campanha (campaign_id).

A documentação interativa dos endpoints pode ser acessada pelo Swagger:

http://127.0.0.1:8000/docs

Estrutura de diretórios

santander_etl/
│
├── api/
│   ├── api.py
│   └── users.json
│
├── data/
│   └── SDW2023.csv
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── ai.py
│   ├── load.py
│   └── email.py
│
├── logs/
│   └── etl.log
│
├── test_ai.py
├── test_extract.py
├── test_load.py
├── test_transform.py
│
├── main.py
├── requirements.txt
├── .env
└── .gitignore

Descrição dos principais arquivos

Arquivo

Responsabilidade

main.py

Orquestra a execução das cinco etapas do pipeline

etl/extract.py

Extração e validação dos dados

etl/transform.py

Consulta, enriquecimento e controle de campanhas

etl/ai.py

Integração com a IA generativa

etl/load.py

Carregamento das mensagens na API

etl/email.py

Envio automático de mensagens por e-mail

api/api.py

Implementação da API REST

api/users.json

Armazenamento dos cadastros e históricos

data/SDW2023.csv

Base de dados de origem

logs/etl.log

Histórico das execuções

requirements.txt

Dependências do projeto

.env

Armazenamento local das credenciais e variáveis de ambiente

.gitignore

Configuração de arquivos ignorados pelo Git

Tecnologias e ferramentas

Python: linguagem principal utilizada no desenvolvimento.

Pandas: leitura e manipulação dos dados estruturados.

FastAPI: construção da API REST.

Requests: comunicação entre as aplicações.

Groq API: integração com Inteligência Artificial Generativa.

Gmail SMTP: envio automatizado de mensagens por e-mail.

python-dotenv: gerenciamento de variáveis de ambiente.

Logging: registro de eventos, informações e erros.

Pytest: execução dos testes automatizados.

Pytest-mock: simulação de respostas e dependências durante os testes.

Git e GitHub: versionamento e publicação do projeto.

Configuração e execução

Pré-requisitos

Python 3.13 ou compatível.

Git.

Conta na GroqCloud.

Chave de API da Groq.

Conta Gmail com configuração de senha de aplicativo para autenticação SMTP.

1. Clonar o repositório

git clone https://github.com/ardesouza/santander-etl-python.git

Acesse a pasta:

cd santander-etl-python

2. Criar o ambiente virtual

python -m venv .venv

Ative o ambiente virtual no Windows PowerShell:

.\.venv\Scripts\Activate.ps1

3. Instalar as dependências

python -m pip install -r requirements.txt

4. Configurar as variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

GROQ_API_KEY=sua_chave_api
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo

Substitua os valores de exemplo pelas credenciais correspondentes:

GROQ_API_KEY: chave de autenticação da API Groq.

EMAIL_USER: endereço Gmail utilizado para envio.

EMAIL_PASSWORD: senha de aplicativo do Gmail.

Importante: nunca compartilhe ou publique suas chaves e senhas. O arquivo .env está protegido pelo .gitignore e não deve ser enviado ao GitHub.

Para utilizar o Gmail, configure uma senha de aplicativo na conta Google, quando disponível. Não utilize a senha normal de acesso à conta.

5. Iniciar a API

Em um terminal, execute:

python -m uvicorn api.api:app --reload

A API estará disponível em:

http://127.0.0.1:8000

6. Executar o pipeline ETL

Abra outro terminal, mantendo o ambiente virtual ativado, e execute:

python main.py

O processo realizará automaticamente as cinco etapas:

Extração dos dados.

Transformação e enriquecimento dos clientes.

Geração de mensagens com IA.

Carregamento das mensagens na API.

Envio dos e-mails aos clientes cadastrados.

O identificador da campanha é definido no arquivo main.py, por meio da variável CAMPAIGN_ID.

Para executar uma nova campanha, utilize um identificador diferente. Clientes que já receberam a campanha identificada não serão processados novamente.

7. Consultar os logs

Os registros da execução são armazenados em:

logs/etl.log

Os logs permitem acompanhar as etapas executadas, quantidades processadas, envios realizados e eventuais erros.

Testes automatizados

O projeto possui testes automatizados desenvolvidos com Pytest, utilizando mocks para simular respostas de APIs e comportamentos externos.

Os testes verificam:

Módulo

Cenários validados

Quantidade

Extração

Leitura correta, arquivo inexistente e colunas ausentes

3

Transformação

Consulta bem-sucedida, campanha já processada e falha de comunicação

3

Inteligência Artificial

Resposta válida, resposta vazia e múltiplos clientes

3

Carregamento

Gravação, duplicidade e falha na API

3

Total



12

Para executar todos os testes:

python -m pytest -v

Resultado da validação

collected 12 items

test_ai.py PASSED
test_extract.py PASSED
test_load.py PASSED
test_transform.py PASSED

12 passed

Os testes utilizam simulações para evitar chamadas desnecessárias à API da Groq e gravações reais durante as validações automatizadas.

Tratamento de erros e confiabilidade

O pipeline implementa mecanismos para melhorar a confiabilidade da execução:

Validação dos dados de entrada.

Verificação da disponibilidade dos arquivos.

Controle de tempo limite nas requisições HTTP.

Tratamento de erros de comunicação.

Prevenção do reprocessamento de campanhas já enviadas.

Controle do histórico de campanhas por cliente.

Tratamento de clientes sem e-mail cadastrado.

Tratamento de falhas durante o envio de e-mails.

Registro de eventos e exceções.

Resumo quantitativo do carregamento e dos envios.

Testes automatizados dos principais cenários.

Proteção das credenciais por meio de variáveis de ambiente.

Considerações finais

Este projeto foi desenvolvido com o objetivo de explorar a aplicação prática de Python na construção de pipelines de dados, demonstrando como diferentes tecnologias podem trabalhar de forma integrada.

A solução reúne extração e transformação de dados, integração de APIs, persistência de informações, utilização de Inteligência Artificial Generativa, controle de campanhas, automação de envio de e-mails e testes de software.

Mais do que demonstrar a execução de um processo ETL, o projeto representa uma oportunidade de aplicar conceitos de engenharia de dados, integração entre sistemas e automação de processos em um cenário prático.

Desenvolvido por Aleksandro Rodrigues

GitHub | Portfólio profissional

[GitHub](https://github.com/ardesouza) | [Portfólio profissional](https://ardesouza.github.io/aleksandrorodrigues/)
