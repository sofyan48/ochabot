# OCHABOT GPT SEARCH
## Description
this project used on my profile page: [iank.me](https://iank.me).
Based on mistral AI, OpenAI, Groq, langchain and chroma vector database, I'm still learning, and this is my first project in AI

## Platform Support
### AI Platform
- OpenAI
- MistralAI
- Groq

### Embedding
- Huggingface
- Mistral
- Nvidia

## Requirements
### Databse
- Redis (LLM Cache and setup)
- Postgree (History)
- ChromaDB (Vector Database)

## How To Run
Running via poetry and activate virtualenvironment
```
poetry shell
```

## Install Requirement
```
poetry install
```

## Environment Setup
```
cp env.example .env
```
please setup APP_ENVIRONTMENT to local if you setup on development mode

## Running 
```
python main.py serve
```
with docker
```
docker compose up --build
```

## Migration
Using Alembic
```
alembic revision --autogenerate -m "Your Table"
```
run migration
```
alembic upgrade head
```

## Swagger
```
http://localhost:8081/docs
```

## Socket
url:
```
localhost:8081/ex/v1/chat/ws/{client_id}
```
payload:
```
{
    "chat": "hello",
    "collection": "ocha_v2",
    "llm": "openai", // optional
    "model": "gpt-4o-mini" // optional
}
```

## Structured Diagram
```mermaid
graph TB
    User((External User))

    subgraph "API Layer"
        FastAPI["API Server<br>(FastAPI)"]
        Router["Router<br>(FastAPI Router)"]
    end

    subgraph "LLM Integration"
        LLMWrapper["AI Wrapper<br>(Python)"]
        subgraph "LLM Providers"
            MistralAI["Mistral AI<br>(API Client)"]
            OpenAI["OpenAI<br>(API Client)"]
            Groq["Groq<br>(API Client)"]
        end
    end

    subgraph "Data Storage"
        ChromaDB["Vector Store<br>(ChromaDB)"]
        Redis["Cache<br>(Redis Stack)"]
        MySQL["Database<br>(MySQL 8.0)"]
    end

    subgraph "Core Components"
        Retriever["Retriever Service<br>(Python)"]
        QnAService["QnA Service<br>(Python)"]
        PromptManager["Prompt Manager<br>(Python)"]
        SetupManager["Setup Manager<br>(Python)"]
    end

    subgraph "Infrastructure"
        K8s["Kubernetes<br>(Helm)"]
        LoadBalancer["Load Balancer<br>(K8s Ingress)"]
        HPA["Auto Scaler<br>(HPA)"]
    end

    %% Relationships
    User -->|"HTTP Requests"| LoadBalancer
    LoadBalancer -->|"Routes"| FastAPI
    FastAPI -->|"Routes Requests"| Router
    
    Router -->|"Handles QnA"| QnAService
    Router -->|"Manages Prompts"| PromptManager
    Router -->|"Manages Setup"| SetupManager
    Router -->|"Handles Retrieval"| Retriever

    QnAService -->|"Uses"| LLMWrapper
    LLMWrapper -->|"Calls"| MistralAI
    LLMWrapper -->|"Calls"| OpenAI
    LLMWrapper -->|"Calls"| Groq

    Retriever -->|"Stores Vectors"| ChromaDB
    QnAService -->|"Caches"| Redis
    SetupManager -->|"Stores Config"| MySQL

    K8s -->|"Manages"| FastAPI
    K8s -->|"Configures"| LoadBalancer
    K8s -->|"Scales"| HPA
```