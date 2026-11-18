# Zentora AI

> **Intelligent AI Workspace — Powered by ROOP**

Zentora AI is a full-stack, enterprise-grade AI assistant and cognitive workspace designed for deep reasoning, real-time multi-format document intelligence (RAG), deterministic mathematical computation, and persistent cross-session memory.

The system pairs a high-performance **Python FastAPI** backend with a responsive **React 19** frontend featuring custom **WebGL2** neural fiber shaders, smooth **Framer Motion** physics, and a cosmic dark glassmorphic design system.

---

## Architecture Overview

```
zentora-ai/
├── FRONTEND/                  # React 19 + Vite Application
│   ├── src/
│   │   ├── components/        # WebGL2 backgrounds, Chat UI, Navigation
│   │   ├── context/           # AuthContext & ChatContext state machines
│   │   ├── hooks/             # useAuth, useChat custom hooks
│   │   ├── pages/             # Landing, Login, Signup, Chat, History, Settings
│   │   └── services/          # Axios interceptors, REST API client, LocalStorage
│   └── vite.config.js         # Optimized Vite bundler configuration
│
└── BACKEND/                   # Python FastAPI Asynchronous Core
    └── app/
        ├── admin/             # System administration & observability
        ├── ai/                # RAG pipeline, LLM providers (Ollama, Gemini, Claude)
        ├── api/               # REST routers (auth, chat, upload, settings, profile)
        ├── core/              # Security, JWT tokens, configuration validation
        ├── database/          # SQLite / SQLAlchemy models and initialization
        ├── repositories/      # Data access layer
        └── main.py            # Application lifespan & CORS middleware
```

---

## Core Capabilities

- **Autonomous Intelligence:** Low-latency conversational processing with dynamic context window scaling.
- **Enterprise Document Intelligence (RAG):** Multimodal document ingestion (`.pdf`, `.docx`, `.txt`, `.csv`), semantic chunking, and high-density vector search with source citations.
- **Symbolic Math & Logic:** Dedicated computation orchestrator designed to handle calculus, algebra, and statistics without hallucinatory drift.
- **Persistent Neural Memory:** Stateful dialogue retention that maintains context, user preferences, and analytical state across sessions.
- **Custom WebGL2 Shaders:** Hardware-accelerated procedural background simulation featuring bloom passes, depth-of-field bokeh, and physics-based cursor interactions.

---

## Technology Stack

### Frontend
- **Framework:** React 19 with Vite 8
- **Styling:** Tailwind CSS with CSS Variables
- **Motion & Physics:** Framer Motion
- **Graphics:** Raw WebGL2 Canvas Shader Pipeline (GLSL 300 es) & Three.js
- **Icons:** Lucide React & React Icons
- **HTTP Client:** Axios with JWT Bearer Interceptors

### Backend
- **Framework:** FastAPI (Python 3.13)
- **Server:** Uvicorn ASGI
- **Data Persistence:** SQLite + SQLAlchemy ORM
- **Vector Embeddings:** ChromaDB / Vector Store
- **Security:** PyJWT, Passlib (Argon2 / BCrypt), OAuth2 Bearer Tokens
- **AI Integrations:** Modular Provider Factory (Ollama local inference, Google Gemini, OpenAI, Anthropic Claude)

---

## Getting Started

### Prerequisites
- **Node.js:** v18.0.0 or higher
- **Python:** v3.11, v3.12, or v3.13
- **Git**

---

### 1. Backend Setup

Open a terminal and navigate to the `BACKEND` directory:

```powershell
cd BACKEND

# 1. Activate the Python virtual environment
.\venv\Scripts\Activate.ps1

# 2. Verify dependencies (if installing fresh: pip install -r requirements.txt)
pip install -r requirements.txt

# 3. Configure environment variables (.env)
# Ensure JWT_SECRET_KEY and AI_PROVIDER are set
cp .env.example .env

# 4. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

The API service will start on **`http://127.0.0.1:8000`**.  
Verify health status at: `http://127.0.0.1:8000/health`  
Interactive OpenAPI documentation is available at: `http://127.0.0.1:8000/docs`

---

### 2. Frontend Setup

Open a second terminal and navigate to the `FRONTEND` directory:

```powershell
cd FRONTEND

# 1. Install dependencies
npm install

# 2. Start the Vite development server
npm run dev
```

The frontend application will be accessible at **`http://localhost:5173`**.

---

## API Endpoints Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/auth/signup` | Register a new user account | No |
| `POST` | `/api/auth/login` | Authenticate user & return JWT token | No |
| `POST` | `/api/chat/` | Submit prompt to AI assistant / RAG pipeline | Yes |
| `GET` | `/api/chat/history/{user_id}` | Retrieve persistent conversation archives | Yes |
| `DELETE` | `/api/chat/{chat_id}` | Delete conversation record | Yes |
| `POST` | `/api/upload/` | Ingest document into vector embedding store | Yes |
| `GET` | `/api/settings/{user_id}` | Fetch user workspace preferences | Yes |
| `PUT` | `/api/settings/{user_id}` | Update workspace preferences (theme, language) | Yes |

---

## Production Build

To compile and optimize the frontend for production deployment:

```powershell
cd FRONTEND
npm run build
```

Production assets will be output to `FRONTEND/dist/` with gzip compression and code splitting.

---

## License

Proprietary — All rights reserved. Designed and developed by **ROOP**.
