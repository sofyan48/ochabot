# OCHABOT GPT OR RAG (RTFM)
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
    Client((Client Application))

    subgraph "Ochabot System"
        subgraph "API Layer"
            FastAPI["API Server<br>(FastAPI)"]
            Router["Router<br>(FastAPI Router)"]
            WebSocket["WebSocket Handler<br>(FastAPI WebSocket)"]
        end

        subgraph "Core Services"
            ChatService["Chat Service<br>(Python)"]
            LLMService["LLM Service<br>(Python)"]
            UserMgmt["User Management<br>(Python)"]
            DocumentIngest["Document Ingestion<br>(Python)"]
            PromptMgmt["Prompt Management<br>(Python)"]
        end

        subgraph "AI Integration Layer"
            AIWrapper["AI Wrapper<br>(Python)"]
            subgraph "LLM Providers"
                MistralAI["Mistral AI<br>(API Client)"]
                OpenAI["OpenAI<br>(API Client)"]
                GroqAI["Groq AI<br>(API Client)"]
            end
        end

        subgraph "Data Storage"
            PostgreSQL[("PostgreSQL<br>(Primary Database)")]
            Redis[("Redis<br>(Cache)")]
            ChromaDB[("ChromaDB<br>(Vector Store)")]
            MinIO[("MinIO<br>(Object Storage)")]
        end

        subgraph "Authentication"
            JWTAuth["JWT Service<br>(Python JWT)"]
            AuthHandler["Auth Handler<br>(FastAPI Auth)"]
        end
    end

    %% External Systems
    subgraph "External Services"
        MistralCloud["Mistral Cloud<br>(AI Service)"]
        OpenAICloud["OpenAI Cloud<br>(AI Service)"]
        GroqCloud["Groq Cloud<br>(AI Service)"]
    end

    %% Connections
    User -->|"Accesses"| FastAPI
    Client -->|"Connects via WebSocket"| WebSocket
    
    FastAPI -->|"Routes requests"| Router
    Router -->|"Handles auth"| AuthHandler
    AuthHandler -->|"Validates"| JWTAuth
    
    Router -->|"Directs"| ChatService
    Router -->|"Directs"| UserMgmt
    Router -->|"Directs"| DocumentIngest
    Router -->|"Directs"| PromptMgmt
    Router -->|"Directs"| LLMService
    
    ChatService -->|"Uses"| AIWrapper
    LLMService -->|"Uses"| AIWrapper
    
    AIWrapper -->|"Calls"| MistralAI
    AIWrapper -->|"Calls"| OpenAI
    AIWrapper -->|"Calls"| GroqAI
    
    MistralAI -->|"Connects to"| MistralCloud
    OpenAI -->|"Connects to"| OpenAICloud
    GroqAI -->|"Connects to"| GroqCloud
    
    DocumentIngest -->|"Stores vectors"| ChromaDB
    DocumentIngest -->|"Stores files"| MinIO
    
    ChatService -->|"Caches"| Redis
    UserMgmt -->|"Stores data"| PostgreSQL
    PromptMgmt -->|"Stores data"| PostgreSQL
    DocumentIngest -->|"Stores metadata"| PostgreSQL
```