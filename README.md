![Galaxy Header](https://raw.githubusercontent.com/iAmNotLins/galaxy-profile/main/assets/generated/galaxy-header.svg)

# TaskForge API

API REST construída com **Python** e **Flask**, containerizada com **Docker** e orquestrada com **Docker Compose**.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12** — runtime
- **Flask** — framework web
- **SQLAlchemy + SQLite** — ORM e banco de dados
- **Gunicorn** — servidor WSGI para produção
- **Docker** — containerização
- **Docker Compose** — orquestração de containers

---

## 📁 Estrutura do Projeto

    TaskForge/
    ├── app/
    │   ├── __init__.py        # App factory (create_app)
    │   ├── app.py             # Ponto de entrada da aplicação
    │   ├── config.py          # Configurações
    │   ├── models/            # Models do SQLAlchemy
    │   └── routes/            # Blueprints do Flask
    ├── instance/
    │   └── taskforge.db       # Banco de dados SQLite (não versionado)
    ├── wsgi.py                # Ponto de entrada do Gunicorn
    ├── dockerfile             # Definição da imagem Docker
    ├── compose.yml            # Orquestração com Docker Compose
    ├── .dockerignore          # Arquivos excluídos do build Docker
    ├── .gitignore             # Arquivos excluídos do Git
    └── requirements.txt       # Dependências Python

---

# 🚀 Como Executar

## Pré-requisitos

- Python **3.12+**
- **Docker**
- **Docker Compose V2** (comando `docker compose` sem hífen)

---

# 1️⃣ Execução Local (sem Docker)

## Clone o repositório

    git clone https://github.com/iamnotlins/taskforge.git
    cd taskforge

---

## Crie e ative o ambiente virtual

    python3 -m venv venv
    source venv/bin/activate

---

## Instale as dependências

    pip install -r requirements.txt

---

## Inicie o servidor de desenvolvimento

    flask run

---

## Teste a API

    curl http://localhost:5000

---

# 2️⃣ Execução com Docker

## Build da imagem

    docker build -t taskforge:v1 .

---

## Subir o container

    docker run -d -p 5000:5000 --name taskforge taskforge:v1

---

## Testar a API

    curl http://localhost:5000

---

## Verificar logs

    docker logs taskforge

---

## Parar e remover o container

    docker rm -f taskforge

---

# 3️⃣ Execução com Docker Compose (Recomendado)

Esta é a forma recomendada de executar o projeto. O **Docker Compose** gerencia o ciclo de vida do container, mapeamento de portas, persistência de dados e política de reinicialização de forma declarativa.

---

## Subir o ambiente

    docker compose up -d

---

## Testar a API

    curl http://localhost:5000

---

## Verificar containers em execução

    docker compose ps

---

## Acompanhar logs em tempo real

    docker compose logs -f

---

## Parar tudo

    docker compose down

---

# 🐳 Detalhes do Docker

## Dockerfile

A imagem é construída a partir de **python:3.12.12-slim** para mantê-la leve.

### Decisões importantes

- `WORKDIR /app` — define o diretório de trabalho dentro do container
- As dependências são instaladas antes de copiar o código-fonte para aproveitar o cache de camadas do Docker
- Um usuário sem privilégios de **root (appuser)** é criado por boas práticas de segurança
- O **Gunicorn** faz o bind em `0.0.0.0:5000` com **3 workers**

---

### Dockerfile

    FROM python:3.12.12-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    RUN groupadd -r appgroup && \
        useradd -r -g appgroup -d /app -s /bin/false appuser

    COPY --chown=appuser:appgroup . .

    EXPOSE 5000

    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]

---

## compose.yml

    services:
      taskforge:
        image: iamnotlins/taskforge:latest
        container_name: taskforge
        ports:
          - "5000:5000"
        volumes:
          - taskforge_data:/app/instance
        restart: unless-stopped

    volumes:
      taskforge_data:

O volume nomeado **taskforge_data** persiste o banco de dados SQLite fora do container — os dados sobrevivem a reinicializações e rebuilds do container.

---

