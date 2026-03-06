![Galaxy Header](https://raw.githubusercontent.com/iAmNotLins/galaxy-profile/main/assets/generated/galaxy-header.svg)

# TaskForge API

API REST construída com Python e Flask, containerizada com Docker e orquestrada com Docker Compose.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12** — runtime
- **Flask** — framework web
- **SQLAlchemy** + **SQLite** — ORM e banco de dados
- **Gunicorn** — servidor WSGI para produção
- **Docker** — containerização
- **Docker Compose** — orquestração de containers

---

## 📁 Estrutura do Projeto

TaskForge/
├── app/
│ ├── init.py # App factory (create_app)
│ ├── app.py # Ponto de entrada da aplicação
│ ├── config.py # Configurações
│ ├── models/ # Models do SQLAlchemy
│ └── routes/ # Blueprints do Flask
├── instance/
│ └── taskforge.db # Banco de dados SQLite (não versionado)
├── wsgi.py # Ponto de entrada do Gunicorn
├── dockerfile # Definição da imagem Docker
├── compose.yml # Orquestração com Docker Compose
├── .dockerignore # Arquivos excluídos do build Docker
├── .gitignore # Arquivos excluídos do Git
└── requirements.txt # Dependências Python

text

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- Docker
- Docker Compose V2 (comando `docker compose` sem hífen)

---

## 1️⃣ Execução Local (sem Docker)

Clone o repositório:

```bash
git clone https://github.com/iamnotlins/taskforge.git
cd taskforge
Crie e ative o ambiente virtual:

bash
python3 -m venv venv
source venv/bin/activate
Instale as dependências:

bash
pip install -r requirements.txt
Inicie o servidor de desenvolvimento:

bash
flask run
Teste a API:

bash
curl http://localhost:5000
2️⃣ Execução com Docker
Build da imagem
bash
docker build -t taskforge:v1 .
Subir o container
bash
docker run -d -p 5000:5000 --name taskforge taskforge:v1
Testar a API
bash
curl http://localhost:5000
Verificar os logs
bash
docker logs taskforge
Parar e remover o container
bash
docker rm -f taskforge
3️⃣ Execução com Docker Compose (recomendado)
Esta é a forma recomendada de executar o projeto. O Docker Compose gerencia o ciclo de vida do container, mapeamento de portas, persistência de dados e política de reinicialização de forma declarativa.

bash
docker compose up -d
Testar a API:

bash
curl http://localhost:5000
Verificar containers em execução:

bash
docker compose ps
Acompanhar logs em tempo real:

bash
docker compose logs -f
Parar tudo:

bash
docker compose down
🐳 Detalhes do Docker
Dockerfile
A imagem é construída a partir do python:3.12.12-slim para mantê-la leve. Decisões importantes:

WORKDIR /app — define o diretório de trabalho dentro do container

As dependências são instaladas antes de copiar o código-fonte para aproveitar o cache de camadas do Docker

Um usuário sem privilégios de root (appuser) é criado por boas práticas de segurança

O Gunicorn faz o bind em 0.0.0.0:5000 com 3 workers

text
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
compose.yml
text
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
O volume nomeado taskforge_data persiste o banco de dados SQLite fora do container — os dados sobrevivem a reinicializações e rebuilds do container.

🐋 Docker Hub
A imagem está disponível publicamente no Docker Hub:

bash
docker pull iamnotlins/taskforge:latest
Para fazer rebuild e publicar uma nova versão:

bash
docker build --no-cache -t taskforge:v2 .
docker tag taskforge:v2 iamnotlins/taskforge:v2
docker tag taskforge:v2 iamnotlins/taskforge:latest
docker push iamnotlins/taskforge:v2
docker push iamnotlins/taskforge:latest
🌿 Estratégia de Branches (Git Flow simplificado)
text
main      → código estável, pronto para "produção"
develop   → branch de integração
feature/* → funcionalidades e correções individuais
Nunca commite diretamente na main. Todas as alterações passam por um Pull Request da develop para a main.

bash
# Sempre parta da develop atualizada
git checkout develop
git pull origin develop
git checkout -b feature/minha-feature

# Após o desenvolvimento
git push origin feature/minha-feature
# Abra o Pull Request: feature/minha-feature → develop
📋 Convenção de Commits
text
feat:     nova funcionalidade
fix:      correção de bug
chore:    configuração / infraestrutura
docs:     documentação
refactor: refatoração sem mudança de comportamento
📝 Licença
MIT

text

Salva como `README.md` na raiz e commita:

```bash
git checkout develop
git checkout -b docs/add-readme
git add README.md
git commit -m "docs: adiciona README com instruções de execução local, docker e compose"
git push origin docs/add-readme
Depois abre o PR docs/add-readme → develop, faz o merge, e quando estiver tudo certo abre o PR develop → main. 🚀
