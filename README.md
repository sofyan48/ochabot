# OCHABOT GPT OR RAG (RTFM)
[![OCHABOT Push to Registry](https://github.com/sofyan48/ochabot/actions/workflows/production.yml/badge.svg?branch=main)](https://github.com/sofyan48/ochabot/actions/workflows/production.yml)
## Description
this project used on my profile page: [iank.me](https://iank.me).
Based on mistral AI, OpenAI, Groq, langchain and chroma vector database, I'm still learning, and this is my first project in AI

## Platform Support
### AI Platform
- OpenAI
- MistralAI
- Groq
- Deepseek
- Ollama

### Embedding
- Huggingface
- Mistral
- Nvidia

## Requirements
### Databse
- Redis (LLM Cache and setup)
- Postgree (History)
- ChromaDB (Vector Database)
### Storage
- Minio

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
alembic revision -m "Your Table"
```
run migration
```
alembic upgrade head
```

## Swagger
```
http://localhost:8081/docs
```

## Default User
```
username: admin
password: admin
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
    
    subgraph "Ochabot System"
        subgraph "API Layer"
            FastAPI["API Server<br>(FastAPI)"]
            Router["Router<br>(FastAPI Router)"]
            WebSocket["WebSocket Handler<br>(FastAPI WebSocket)"]
            
            subgraph "API Components"
                ChatHandler["Chat Handler<br>(Python)"]
                UserHandler["User Handler<br>(Python)"]
                IngestHandler["Ingest Handler<br>(Python)"]
                PromptHandler["Prompt Handler<br>(Python)"]
                SetupHandler["Setup Handler<br>(Python)"]
                ClientHandler["Client Handler<br>(Python)"]
                LoginHandler["Login Handler<br>(Python)"]
            end
        end

        subgraph "LLM Services"
            LLMWrapper["LLM Wrapper<br>(Python)"]
            
            subgraph "LLM Providers"
                OpenAI["OpenAI Service<br>(OpenAI API)"]
                Mistral["Mistral Service<br>(Mistral API)"]
                Groq["Groq Service<br>(Groq API)"]
                DeepSeek["DeepSeek Service<br>(DeepSeek API)"]
                Ollama["Ollama Service<br>(Ollama API)"]
            end
        end

        subgraph "Data Storage"
            PostgreSQL[("PostgreSQL<br>(Primary Database)")]
            Redis[("Redis<br>(Cache)")]
            MinIO[("MinIO<br>(Object Storage)")]
            ChromaDB[("ChromaDB<br>(Vector Store)")]
        end

        subgraph "Core Services"
            DatabaseService["Database Service<br>(SQLAlchemy)"]
            VectorService["Vector Store Service<br>(LangChain)"]
            CacheService["Cache Service<br>(Redis Stack)"]
            StorageService["Storage Service<br>(MinIO)"]
        end
    end

    %% Connections
    User -->|"HTTP/WebSocket"| FastAPI
    FastAPI -->|"Routes"| Router
    Router -->|"Handles WebSocket"| WebSocket
    
    %% API Components connections
    Router --> ChatHandler
    Router --> UserHandler
    Router --> IngestHandler
    Router --> PromptHandler
    Router --> SetupHandler
    Router --> ClientHandler
    Router --> LoginHandler

    %% LLM Service connections
    ChatHandler --> LLMWrapper
    LLMWrapper --> OpenAI
    LLMWrapper --> Mistral
    LLMWrapper --> Groq
    LLMWrapper --> DeepSeek
    LLMWrapper --> Ollama

    %% Data Storage connections
    DatabaseService --> PostgreSQL
    CacheService --> Redis
    StorageService --> MinIO
    VectorService --> ChromaDB

    %% Service Usage connections
    ChatHandler --> DatabaseService
    UserHandler --> DatabaseService
    IngestHandler --> DatabaseService
    PromptHandler --> DatabaseService
    SetupHandler --> DatabaseService
    ClientHandler --> DatabaseService
    LoginHandler --> DatabaseService

    ChatHandler --> VectorService
    IngestHandler --> VectorService
    
    ChatHandler --> CacheService
    UserHandler --> CacheService
    
    IngestHandler --> StorageService
```