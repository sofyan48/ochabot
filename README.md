# OCHABOT GPT SEARCH (RTFM)
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
            FastAPI["API Server<br>FastAPI"]
            Router["Router<br>FastAPI Router"]
            CORS["CORS Middleware<br>Starlette"]
            WebSocket["WebSocket Handler<br>FastAPI WebSocket"]
        end

        subgraph "Core Services"
            AuthService["Authentication Service<br>JWT"]
            ChatService["Chat Service<br>Python"]
            LLMService["LLM Service<br>Python"]
            UserService["User Service<br>Python"]
            PromptService["Prompt Service<br>Python"]
            RetrievalService["Retrieval Service<br>Python"]
        end

        subgraph "LLM Integration"
            LLMWrapper["LLM Wrapper<br>Python"]
            MistralAI["Mistral Integration<br>Python"]
            OpenAI["OpenAI Integration<br>Python"]
            GroqAI["Groq Integration<br>Python"]
            Prompter["Prompt Chain<br>LangChain"]
        end

        subgraph "Data Layer"
            PostgreSQL[("PostgreSQL<br>Database")]
            Redis[("Redis<br>Cache")]
            MinIO[("MinIO<br>Object Storage")]
            ChromaDB[("ChromaDB<br>Vector Store")]
        end
    end

    subgraph "External Services"
        MistralAPI["Mistral AI API<br>External Service"]
        OpenAIAPI["OpenAI API<br>External Service"]
        GroqAPI["Groq API<br>External Service"]
    end

    %% Connections
    User -->|"HTTP/WebSocket"| FastAPI
    FastAPI -->|"Routes"| Router
    FastAPI -->|"Uses"| CORS
    FastAPI -->|"WebSocket"| WebSocket

    Router -->|"Auth"| AuthService
    Router -->|"Chat"| ChatService
    Router -->|"Users"| UserService
    Router -->|"Prompts"| PromptService
    Router -->|"Retrieval"| RetrievalService

    ChatService --> LLMService
    LLMService --> LLMWrapper
    LLMWrapper -->|"Uses"| MistralAI
    LLMWrapper -->|"Uses"| OpenAI
    LLMWrapper -->|"Uses"| GroqAI
    LLMWrapper -->|"Uses"| Prompter

    MistralAI -->|"API Calls"| MistralAPI
    OpenAI -->|"API Calls"| OpenAIAPI
    GroqAI -->|"API Calls"| GroqAPI

    AuthService -->|"Read/Write"| PostgreSQL
    UserService -->|"Read/Write"| PostgreSQL
    PromptService -->|"Read/Write"| PostgreSQL
    
    ChatService -->|"Cache"| Redis
    RetrievalService -->|"Vectors"| ChromaDB
    ChatService -->|"Files"| MinIO

    %% Component relationships
    subgraph "Database Components"
        DBPool["Connection Pool<br>SQLAlchemy"]
        DBMigrations["Migrations<br>Alembic"]
    end
    PostgreSQL --- DBPool
    PostgreSQL --- DBMigrations
```