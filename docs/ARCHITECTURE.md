# Velora-AI System Architecture

## 1. Purpose

This document describes the current architectural direction of Velora-AI and the target architecture for its production-ready release.

Existing components must be verified against the source code before being treated as completed implementation.

## 2. Architecture Principles

- Modular and maintainable code.
- Clear separation of frontend, backend, and data layers.
- Secure authentication and authorization.
- Strict user-level data isolation.
- Replaceable AI providers.
- Reliable error handling and logging.
- Automated testing before release.
- Environment-based configuration.
- No secrets or credentials committed to source control.

## 3. High-Level System Architecture

The target system consists of these major components:

1. Frontend application
2. Backend API
3. Authentication and authorization
4. AI orchestration layer
5. AI provider integrations
6. Agent and tool execution
7. Conversation and memory services
8. Document processing and retrieval
9. Mathematical computation engine
10. Database and persistent storage
11. Monitoring and deployment infrastructure

## 4. Frontend Architecture

Technology direction:

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- React Icons

Responsibilities:

- User registration and login.
- Protected application routes.
- AI chat interface.
- Conversation history.
- Document upload interface.
- User profile and settings.
- Administrative interface.
- API communication.
- Loading, error, and empty states.

The frontend must not contain private API keys, database credentials, or authorization secrets.

## 5. Backend Architecture

Technology direction:

- Python
- FastAPI
- Pydantic
- SQLAlchemy

Responsibilities:

- API request validation.
- Authentication and authorization.
- User and conversation management.
- AI orchestration.
- Provider selection.
- Agent and tool execution.
- Memory management.
- Document processing.
- Mathematical computation.
- Database operations.
- Logging and error handling.

Routes should remain separate from business logic and database access.

## 6. Authentication and Authorization

Target authentication flow:

1. User submits registration details.
2. Backend validates the request.
3. Password is securely hashed.
4. User record is stored.
5. User submits login credentials.
6. Backend verifies the password.
7. Backend issues an authentication token.
8. Frontend stores the token using an appropriate secure strategy.
9. Protected requests include valid authentication.
10. Backend verifies the identity and permissions.

Security requirements:

- Passwords must never be stored in plaintext.
- Tokens must be signed using environment-configured secrets.
- Protected endpoints must validate ownership.
- Administrative permissions must be checked server-side.
- Users must not access another user's private data.

## 7. AI Orchestration

The AI orchestration layer coordinates requests between the API, agents, tools, memory, and AI providers.

Target request flow:

1. Receive the user's message.
2. Authenticate the user.
3. Validate the conversation and request.
4. Identify the appropriate processing path.
5. Retrieve permitted conversation context.
6. Execute relevant tools or agents.
7. Select an AI provider when required.
8. Generate the response.
9. Persist the conversation.
10. Return the result to the frontend.

Tool execution and deterministic computations should be separated from ordinary language generation.

## 8. AI Provider Architecture

The provider layer should allow different AI services to be used without changing the main application logic.

Planned providers:

- Ollama for local development.
- OpenAI for hosted inference.
- Gemini for hosted inference.
- Groq for hosted inference.
- Additional providers when justified.

Provider credentials must be loaded from environment variables.

Provider failures, timeouts, unavailable models, and invalid responses must be handled safely.

The production provider must be selected and tested before deployment.

## 9. Agent and Tool Architecture

Agents coordinate specialized tasks.

Tools perform specific operations.

Potential tool categories:

- Mathematical computation.
- Date and time.
- Document retrieval.
- Information extraction.
- Other validated application capabilities.

Tools must have defined input validation, output formats, execution limits, and error handling.

The system must not execute arbitrary user-supplied code or shell commands without a properly isolated and secured execution environment.

## 10. Conversation and Memory Architecture

Conversation storage and persistent memory are separate responsibilities.

Conversation storage:

- Stores chat sessions.
- Stores user and assistant messages.
- Supports history retrieval.
- Supports conversation deletion.
- Enforces user ownership.

Memory:

- Stores explicitly supported information across conversations.
- Retrieves only information belonging to the authenticated user.
- Supports updates and deletion.
- Applies retention and privacy rules.

In-memory conversation context is not a replacement for persistent storage.

## 11. Document Intelligence and RAG

Target document workflow:

1. Authenticate the user.
2. Validate the uploaded file.
3. Enforce file size and type restrictions.
4. Extract document text.
5. Split text into manageable chunks.
6. Generate embeddings.
7. Store chunks with user and document ownership metadata.
8. Retrieve relevant chunks for a query.
9. Filter retrieval by authenticated user.
10. Generate an answer grounded in retrieved content.

Document access must be isolated between users.

Uploaded files and extracted content must be handled according to defined security and retention policies.

## 12. Mathematical Computation Engine

The mathematical engine should handle supported deterministic operations independently of language-model calculations.

Initial supported areas:

- Arithmetic.
- Algebraic expressions.
- Equation solving.
- Differentiation.
- Matrix operations.

SymPy may be used for supported symbolic operations.

Unsupported or ambiguous inputs must produce clear errors instead of fabricated results.

Every supported operation requires automated tests.

## 13. Database Architecture

Initial development may use SQLite.

Production target:

- PostgreSQL.
- SQLAlchemy.
- Database migrations.
- Proper indexes and constraints.
- Transaction management.

Core data entities should include:

- Users.
- Conversations.
- Messages.
- User profiles.
- Uploaded documents.
- Document chunks.
- Memory records.
- Administrative records where required.

The final schema must be verified against the actual models and migrations.

## 14. API Architecture

The backend should expose versionable, documented REST endpoints.

Major API areas:

- Authentication.
- Chat.
- Conversation history.
- User profile.
- Document uploads.
- Memory.
- Administrative operations.
- Health checks.

All protected endpoints must enforce authentication and authorization.

API documentation should accurately describe request schemas, response schemas, and error responses.

## 15. Security Architecture

Required controls:

- Environment-based secrets.
- Secure password hashing.
- JWT validation.
- CORS allowlist.
- Request validation.
- Rate limiting.
- File upload validation.
- User-level resource ownership.
- Database access controls.
- Safe exception handling.
- Dependency vulnerability checks.
- No sensitive information in logs.

Security controls must be verified through tests.

## 16. Deployment Architecture

Target deployment direction:

- Frontend: Vercel.
- Backend: Render or an equivalent hosting platform.
- Database: Managed PostgreSQL.
- AI inference: A supported hosted provider.

Local Ollama must not be assumed to be accessible from a remote backend deployment.

Production configuration must use environment variables and must not depend on local development paths.

## 17. Testing Strategy

Testing should cover:

- Unit tests.
- API integration tests.
- Authentication tests.
- Authorization and ownership tests.
- Database tests.
- AI provider tests.
- Mathematical correctness tests.
- Document retrieval isolation tests.
- Frontend integration tests.
- Production smoke tests.

A feature is complete only after its expected behavior has been tested.

## 18. Architecture Verification Status

This document defines the target architecture.

The following areas require source-level verification before being marked production-ready:

- Frontend and backend API integration.
- Authentication consistency.
- Authorization and resource ownership.
- Database schema and migrations.
- AI provider reliability.
- Memory persistence and isolation.
- RAG retrieval isolation.
- Mathematical correctness.
- Automated test coverage.
- Production configuration.

## 19. Maintenance

Update this document whenever a significant architectural decision or implementation change is made.

Do not document planned functionality as verified functionality.
