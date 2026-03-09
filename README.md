# TaskForge API — Enterprise Security Edition v3

API REST construída com **Python/Flask**, agora com **segurança enterprise-grade**.

- **0 Critical/High CVEs** (Trivy + Docker Scout)
- **Assinatura Cosign** (digest SHA256)
- **Container non-root** (CIS Benchmark 4.1)
- **Git Flow com tags versionadas**

---

# 🛡️ Status de Segurança — v3

| Verificação | Status | Comando |
|---|---|---|
| Vulnerabilidades | ✅ 0 Critical/High | trivy iamnotlins/taskforge:v3 |
| Assinatura | ✅ Válida | cosign verify iamnotlins/taskforge:v3 |
| Non-root | ✅ appuser UID 1000 | docker run taskforge:v3 id |
| Git Tag | ✅ v3 | git tag v3 |

---

# 🛠️ Tecnologias Utilizadas

- **Python 3.14.3-alpine3.23** — base image segura (18MB)
- **Flask** — framework web
- **Gunicorn** — WSGI production server
- **SQLite** — banco leve para desenvolvimento
- **Docker** — containerização
- **Docker Compose** — orquestração
- **Cosign** — assinatura criptográfica
- **Trivy** — scanner de vulnerabilidades

---

# 📁 Estrutura do Projeto

    TaskForge/
    ├── app/                     # Flask application
    ├── docs/security/           # 🔒 Documentação de segurança
    │   ├── keys/cosign.pub      # Chave pública para verificação
    │   └── release-v3.md        # Histórico das correções
    ├── .trivyignore             # CVEs aceitos com justificativa
    ├── .gitignore               # cosign.key protegida
    ├── dockerfile               # Imagem Alpine + non-root
    ├── compose.yml              # Orquestração production-ready
    └── requirements.txt         # Dependências versionadas

---

# 🚀 Como Executar

## 🔐 Pré-requisitos de Segurança

Verificar a imagem antes de usar.

    docker scout cves iamnotlins/taskforge:v3
    trivy image --ignorefile .trivyignore iamnotlins/taskforge:v3
    cosign verify --key docs/security/keys/cosign.pub iamnotlins/taskforge:v3

---

# 1️⃣ Docker Compose (Recomendado)

## Subir ambiente production-like

    docker compose up -d

---

## Testar API

    curl http://localhost:5000

---

## Logs em tempo real

    docker compose logs -f

---

## Parar ambiente

    docker compose down

---

# 2️⃣ Container Único

    docker run -d -p 5000:5000 --name taskforge iamnotlins/taskforge:v3

    curl http://localhost:5000

    docker logs taskforge

    docker rm -f taskforge

---

# 3️⃣ Build Local (Desenvolvimento)

## Build da imagem local

    docker build -t taskforge:local .

---

## Testar antes de publicar

    docker scout cves taskforge:local
    trivy image taskforge:local
    docker run -p 5000:5000 taskforge:local

---

# 🐳 Docker Security Details

## Dockerfile v3 — Production Hardened

    FROM python:3.14.3-alpine3.23    # 18MB, 0 Critical CVEs

    RUN apk upgrade --no-cache      # OS patches
    RUN pip install --upgrade pip   # Fix CVE-2026-1703

    RUN addgroup -S appgroup && adduser -S -G appgroup appuser   # Alpine native

    USER appuser                    # CIS 4.1 - Non-root

    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]

---

# Principais Correções Aplicadas

| Problema v1 | Correção v3 | Impacto |
|---|---|---|
| python:3.11 full | python:3.14.3-alpine3.23 | -24MB, -20 CVEs |
| groupadd/useradd | addgroup/adduser | Build compatível Alpine |
| Sem USER | USER appuser | Non-root execution |
| pip 25.3 | pip 26.0 | CVE-2026-1703 corrigida |

---

# 🔍 Verificações de Segurança

## Scan de Vulnerabilidades

### Scanner primário (Docker nativo)

    docker scout cves iamnotlins/taskforge:v3

---

### Scanner secundário (cobertura cruzada)

    trivy image --ignorefile .trivyignore iamnotlins/taskforge:v3

---

### Detectar secrets hardcoded

    trivy image --scanners secret iamnotlins/taskforge:v3

---

# Verificar Assinatura Cosign

    cosign verify --key docs/security/keys/cosign.pub iamnotlins/taskforge:v3

---

## Output esperado

    The cosign claims were validated
    Existence in transparency log verified
    Signatures match public key

---

# 📈 Versionamento e Releases

| Tag | Status | GitHub | Docker Hub |
|---|---|---|---|
| v1 | Legacy (CVEs) | git tag v1 | iamnotlins/taskforge:v1 |
| v2 | Obsoleta | - | iamnotlins/taskforge:v2 |
| v3 | Production | git tag v3 | iamnotlins/taskforge:v3 |

---

# Digest SHA256 (imutável)

    sha256:f0e7ecebf1b0bc8c2589082e06a8403a99433fbe358f14509b4aa214be1cc43f

---

# ⚙️ Git Flow Configurado

    main ──●─(v3)─●          # Produção
    develop ───●──────────── # Desenvolvimento

Próximas features:

    develop → feature/xxx → merge → main → tag

---


# 🚀 Quick Start (1 comando)

    git clone https://github.com/iamnotlins/taskforge.git &&
    cd taskforge &&
    docker compose up -d &&
    curl http://localhost:5000

---
