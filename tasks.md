Okay, this is a fantastic approach for leveraging an engineering LLM. An extremely granular, testable plan is key.

Here's a step-by-step plan to build the MVP of Project "Aura," focusing on the absolute core: uploading a single document, processing it, and asking a question against it using a very basic RAG flow. Each task is designed to be small, testable, and address a single concern.

---

## MVP Build Plan: Project "Aura"

**Overall MVP Goal:** A user can register, log in, upload one PDF document, and ask a simple question about that document. The system will retrieve relevant text chunks from the document and use an LLM to generate an answer.

---

### Phase 0: Project Setup & Core Backend Infrastructure

* **Task ID: P0-T1**
    * **Description:** Initialize project directory structure for the backend. - [x]
    * **Start State:** Empty directory.
    * **End State:** Directory `aura-backend/` created with subdirectories `app/`, `tests/`. `aura-backend/app/` contains an empty `main.py`.
    * **Test:** Verify directory structure exists. `python aura-backend/app/main.py` runs without error (even if it does nothing).

* **Task ID: P0-T2**
    * **Description:** Set up a virtual environment and install FastAPI & Uvicorn. - [x]
    * **Start State:** `aura-backend/` directory exists.
    * **End State:** Python virtual environment created and activated. `fastapi` and `uvicorn` installed. `requirements.txt` created/updated.
    * **Test:** Run `uvicorn app.main:app --reload` from within `aura-backend/` and see the server start.

* **Task ID: P0-T3**
    * **Description:** Create a basic "Hello World" GET endpoint in `app/main.py`. - [x]
    * **Start State:** FastAPI app can start but has no endpoints.
    * **End State:** `/` endpoint returns `{"message": "Hello World"}`.
    * **Test:** Navigate to `http://127.0.0.1:8000/` in a browser or use `curl` and see the JSON response.

* **Task ID: P0-T4**
    * **Description:** Set up basic project configuration (`app/core/config.py`) for environment variables (e.g., `PROJECT_NAME`, `API_V1_STR`). - [x]
    * **Start State:** No central configuration management.
    * **End State:** `config.py` created. Settings class (e.g., Pydantic's `BaseSettings`) loads variables from a `.env` file. `main.py` can access these settings.
    * **Test:** Print `PROJECT_NAME` on server startup or in the "Hello World" response; verify it matches `.env`.

* **Task ID: P0-T5**
    * **Description:** Initialize Git repository for the backend. - [x]
    * **Start State:** No version control.
    * **End State:** `aura-backend/` is a Git repository with an initial commit including all current files and a `.gitignore` file (ignoring `__pycache__`, `.env`, `venv/`).
    * **Test:** `git status` shows a clean working tree.

---

### Phase 1: User Authentication & Basic Data Models (PostgreSQL)

* **Task ID: P1-T1**
    * **Description:** Set up Docker and run a PostgreSQL container. - [x]
    * **Start State:** No database running.
    * **End State:** PostgreSQL container is running and accessible. Database connection details (host, port, user, password, db_name) are in `.env`.
    * **Test:** Connect to the PostgreSQL instance using `psql` or a GUI tool (e.g., DBeaver, pgAdmin) with credentials from `.env`.

* **Task ID: P1-T2**
    * **Description:** Install SQLAlchemy, SQLModel (or chosen ORM), psycopg2-binary, and Alembic. - [x]
    * **Start State:** No database libraries in `requirements.txt`.
    * **End State:** Libraries installed and added to `requirements.txt`.
    * **Test:** Python interpreter can import `sqlalchemy`, `sqlmodel`, `alembic`.

* **Task ID: P1-T3**
    * **Description:** Create database session management (`app/db/session.py`) to connect to PostgreSQL. - [x]
    * **Start State:** No code to connect to PostgreSQL.
    * **End State:** `session.py` provides a SQLAlchemy/SQLModel engine instance and a way to get a DB session (e.g., `get_db` dependency).
    * **Test:** A test script can successfully connect to the PostgreSQL container using `session.py`.

* **Task ID: P1-T4**
    * **Description:** Define a `User` model (`app/db/models_pg.py`) with fields: `id` (PK, auto-increment/UUID), `email` (unique), `hashed_password`, `is_active`. - [x]
    * **Start State:** No User model.
    * **End State:** `User` SQLModel/SQLAlchemy model defined.
    * **Test:** Model definition is syntactically correct.

* **Task ID: P1-T5**
    * **Description:** Initialize Alembic for database migrations. - [x]
    * **Start State:** No migration tool configured.
    * **End State:** Alembic environment configured in the project. A `migrations/` directory is created.
    * **Test:** `alembic revision -m "initial_setup"` runs successfully.

* **Task ID: P1-T6**
    * **Description:** Generate an initial Alembic migration for the `User` table. - [x]
    * **Start State:** `User` model defined but no corresponding table in DB.
    * **End State:** Alembic migration script created that defines the `users` table.
    * **Test:** Review generated migration script for correctness.

* **Task ID: P1-T7**
    * **Description:** Apply the Alembic migration to create the `users` table in PostgreSQL. - [x]
    * **Start State:** `users` table does not exist in the database.
    * **End State:** `users` table exists in the database with the correct schema.
    * **Test:** Inspect the database schema using `psql` or a GUI tool to confirm table creation.

* **Task ID: P1-T8**
    * **Description:** Create Pydantic schemas for User creation and User display (`app/schemas/user_schemas.py`). - [x]
    * **Start State:** No user-related Pydantic schemas.
    * **End State:** `UserCreate` (email, password) and `UserRead` (id, email, is_active) schemas defined.
    * **Test:** Schemas are syntactically correct and can be imported.

* **Task ID: P1-T9**
    * **Description:** Create password hashing utilities (`app/core/security.py`) using `passlib` (e.g., `get_password_hash`, `verify_password`). - [x]
    * **Start State:** No password hashing.
    * **End State:** `security.py` provides functions for hashing and verifying passwords.
    * **Test:** Unit test: hash a password, verify it against the original.

* **Task ID: P1-T10**
    * **Description:** Create a CRUD operation to create a user (`app/crud/crud_user.py`). - [x]
    * **Start State:** No way to add users to the DB programmatically.
    * **End State:** `crud_user.create_user(db, user: UserCreate)` function saves a new user with a hashed password.
    * **Test:** Unit test: call `create_user`, then query DB directly to verify user existence and hashed password.

* **Task ID: P1-T11**
    * **Description:** Create a `/users/` POST endpoint for user registration (`app/api/v1/auth.py`). - [x]
    * **Start State:** No registration endpoint.
    * **End State:** Endpoint accepts `UserCreate` schema, calls `crud_user.create_user`, returns `UserRead` schema.
    * **Test:** Send POST request with valid user data, expect 201 Created and user data. Send duplicate email, expect error.

* **Task ID: P1-T12**
    * **Description:** Create a CRUD operation to get a user by email (`app/crud/crud_user.py`). - [x]
    * **Start State:** No way to fetch a user by email.
    * **End State:** `crud_user.get_user_by_email(db, email: str)` function retrieves a user.
    * **Test:** Unit test: create a user, then fetch by email.

* **Task ID: P1-T13**
    * **Description:** Implement JWT token creation (`app/core/security.py`). - [x]
    * **Start State:** No JWT functionality.
    * **End State:** `create_access_token(data: dict)` function generates a JWT. `SECRET_KEY` and `ALGORITHM` defined in `config.py`.
    * **Test:** Unit test: create a token, decode it (without verifying signature for this test, just structure), check payload.

* **Task ID: P1-T14**
    * **Description:** Create a `/login/access-token` POST endpoint (`app/api/v1/auth.py`) using FastAPI's `OAuth2PasswordRequestForm`. - [x]
    * **Start State:** No login endpoint.
    * **End State:** Endpoint authenticates user (using `get_user_by_email` and `verify_password`), returns JWT access token.
    * **Test:** Register a user. Attempt login with correct credentials, expect token. Attempt with incorrect credentials, expect error.

* **Task ID: P1-T15**
    * **Description:** Implement a dependency to get the current active user from JWT (`app/api/deps.py` or `app/core/security.py`). - [x]
    * **Start State:** No way to protect endpoints or get current user.
    * **End State:** `get_current_active_user` dependency decodes JWT from Authorization header, retrieves user from DB, and checks if active.
    * **Test:** Create a test protected endpoint. Call it without token (expect 401). Call with valid token (expect success). Call with token for inactive user (expect 400/403).

* **Task ID: P1-T16**
    * **Description:** Create a `/users/me` GET endpoint to test authentication (`app/api/v1/users.py`). - [x]
    * **Start State:** No authenticated endpoint to retrieve user info.
    * **End State:** Endpoint uses `get_current_active_user` dependency and returns the current user's details (`UserRead` schema).
    * **Test:** Log in to get a token. Call `/users/me` with the token, expect current user details.

---

### Phase 2: Initial Document Handling (No AI Yet)

* **Task ID: P2-T1**
    * **Description:** Define a `Document` model (`app/db/models_pg.py`) in PostgreSQL with fields: `id`, `file_name`, `s3_key` (or `file_path` for local storage for MVP), `upload_timestamp`, `status` (e.g., "PENDING", "PROCESSING", "COMPLETED", "FAILED"), `user_id` (FK to User). - [x]
    * **Start State:** No Document model.
    * **End State:** `Document` SQLModel/SQLAlchemy model defined.
    * **Test:** Model definition is syntactically correct.

* **Task ID: P2-T2**
    * **Description:** Generate and apply Alembic migration for the `Document` table. - [x]
    * **Start State:** `Document` model defined but no table in DB.
    * **End State:** `documents` table exists in PostgreSQL.
    * **Test:** Inspect DB to confirm `documents` table creation and schema.

* **Task ID: P2-T3**
    * **Description:** Create Pydantic schemas for Document (`app/schemas/document_schemas.py`) e.g., `DocumentRead`, `DocumentCreateResponse`. - [x]
    * **Start State:** No document-related Pydantic schemas.
    * **End State:** Schemas defined.
    * **Test:** Schemas are syntactically correct.

* **Task ID: P2-T4**
    * **Description:** Create a CRUD operation to create a document record (`app/crud/crud_document.py`). - [x]
    * **Start State:** No way to add document metadata to DB.
    * **End State:** `crud_document.create_document(db, file_name, file_path, user_id)` function saves document metadata.
    * **Test:** Unit test: call `create_document`, query DB to verify record.

* **Task ID: P2-T5**
    * **Description:** Implement a simple file storage mechanism (local `/uploads` directory). - [x]
    * **Start State:** No file storage.
    * **End State:** `/uploads` directory created (and gitignored). Function to save `UploadFile` to this directory, returning the path.
    * **Test:** Unit test: save a dummy file, verify it exists at the expected path.

* **Task ID: P2-T6**
    * **Description:** Create a `/documents/upload` POST endpoint. - [x]
    * **Start State:** No document upload endpoint.
    * **End State:** Endpoint:
        1.  Requires authenticated user (uses `get_current_active_user`).
        2.  Accepts `UploadFile`.
        3.  Saves the file using the mechanism from P2-T5.
        4.  Creates a `Document` record in PostgreSQL using `crud_document.create_document` with status "PENDING".
        5.  Returns `DocumentCreateResponse` (e.g., document ID, file name, status).
    * **Test:** Log in, upload a small PDF file. Verify file saved in `/uploads`. Verify record in `documents` table. Verify JSON response.

---

### Phase 2.5: Testing Foundation

* **Task ID: P2.5-T1**
    * **Description:** Install `pytest` and `httpx` for API testing. - [x]

* **Task ID: P2.5-T2**
    * **Description:** Create a pytest fixture for a test database session. - [x]

* **Task ID: P2.5-T3**
    * **Description:** Create a pytest fixture for an authenticated test client. - [x]

* **Task ID: P2.5-T4**
    * **Description:** Write API tests for user authentication (`tests/api/v1/test_auth.py`). - [x]

* **Task ID: P2.5-T5**
    * **Description:** Write API tests for the document upload endpoint (`tests/api/v1/test_documents.py`). - [x]

---

### Phase 3: Core Knowledge Representation - Neo4j & Vector Store Setup

* **Task ID: P3-T1**
    * **Description:** Set up Docker and run a Neo4j container.
    * **Start State:** No graph database running.
    * **End State:** Neo4j container is running and accessible via Bolt port and HTTP port (for Browser). Connection details in `.env`.
    * **Test:** Connect to Neo4j Browser (`http://localhost:7474`) and run a simple Cypher query (e.g., `MATCH (n) RETURN n LIMIT 1`).

* **Task ID: P3-T2**
    * **Description:** Install Neo4j Python driver (`neo4j`).
    * **Start State:** No Neo4j driver.
    * **End State:** Library installed and added to `requirements.txt`.
    * **Test:** Python interpreter can import `neo4j`.

* **Task ID: P3-T3**
    * **Description:** Create Neo4j connection management (`app/services/knowledge_graph_service.py` or `app/db/graph_session.py`).
    * **Start State:** No code to connect to Neo4j.
    * **End State:** Service/module provides a Neo4j driver instance and functions to run read/write Cypher queries. Credentials from `config.py`.
    * **Test:** A test script can connect to Neo4j and execute `RETURN 1 AS result`.

* **Task ID: P3-T4**
    * **Description:** Define a very simple V1 Neo4j schema: A `DocumentChunk` node with properties `id` (UUID), `text`, `document_id_pg` (FK to PostgreSQL `documents.id`), `chunk_seq_num`.
    * **Start State:** No defined Neo4j schema for chunks.
    * **End State:** Conceptual schema defined (documented in code comments or a design doc).
    * **Test:** N/A (conceptual).

* **Task ID: P3-T5**
    * **Description:** Create a function in `knowledge_graph_service.py` to create a `DocumentChunk` node in Neo4j.
    * **Start State:** No function to add `DocumentChunk` nodes.
    * **End State:** `create_document_chunk_node(tx, chunk_id, text, document_id_pg, chunk_seq_num)` function exists.
    * **Test:** Unit test: call the function within a Neo4j transaction, verify node creation with properties using Neo4j Browser or a Cypher query.

* **Task ID: P3-T6**
    * **Description:** Set up a Vector Database (e.g., ChromaDB running in Docker, or a cloud-based one like Pinecone with a free tier). For ChromaDB, install `chromadb`.
    * **Start State:** No vector database.
    * **End State:** Vector DB is running/accessible. Connection details/API key in `.env`. `chromadb` (or other client) installed.
    * **Test:** A test script can connect to the vector DB and create/check a test collection.

* **Task ID: P3-T7**
    * **Description:** Create vector DB connection management (`app/services/vector_store_service.py`).
    * **Start State:** No code to connect to vector DB.
    * **End State:** Service provides functions to connect, add embeddings (with metadata and IDs), and query by vector.
    * **Test:** Unit test: add a test vector with metadata, then query for it.

---

### Phase 4: Document Processing & Basic RAG (Core of MVP)

* **Task ID: P4-T1**
    * **Description:** Install Celery and a message broker (e.g., Redis). Run Redis in Docker.
    * **Start State:** No async task queue.
    * **End State:** `celery` and `redis` Python libraries installed. Redis container running. Celery configured in `app/worker.py` and `app/core/config.py` to use Redis broker.
    * **Test:** A simple Celery "add(x, y)" task can be defined, called via `.delay()`, and a Celery worker (run locally) picks it up and executes it (logs output).

* **Task ID: P4-T2**
    * **Description:** Install PDF parsing library (e.g., `PyMuPDF`).
    * **Start State:** No PDF parsing capability.
    * **End State:** `PyMuPDF` installed and added to `requirements.txt`.
    * **Test:** A test script can open a sample PDF and extract all text from it.

* **Task ID: P4-T3**
    * **Description:** Implement a simple text chunking function (`app/services/document_processing_service.py`).
    * **Start State:** No text chunking logic.
    * **End State:** `chunk_text(text: str, chunk_size: int, overlap: int)` function splits text into overlapping chunks.
    * **Test:** Unit test: pass sample text, verify output chunks meet size/overlap criteria.

* **Task ID: P4-T4**
    * **Description:** Install OpenAI Python client (`openai`). Add `OPENAI_API_KEY` to `.env`.
    * **Start State:** No OpenAI client.
    * **End State:** Library installed. API key configured.
    * **Test:** A test script can make a simple API call (e.g., list models, or a cheap embedding).

* **Task ID: P4-T5**
    * **Description:** Implement a function to get text embeddings using OpenAI API (`app/services/llm_service.py` or embed in `document_processing_service.py`).
    * **Start State:** No embedding logic.
    * **End State:** `get_embeddings(texts: List[str])` function returns a list of embeddings.
    * **Test:** Unit test: pass a list with one short string, verify an embedding vector is returned with expected dimensionality.

* **Task ID: P4-6**
    * **Description:** Create a Celery task `process_document_for_mvp(document_id_pg: int, file_path: str)` in `app/tasks/process_document.py`.
    * **Start State:** Document upload creates a "PENDING" record but no processing happens.
    * **End State:** Celery task definition exists.
    * **Test:** N/A (task definition only).

* **Task ID: P4-T7**
    * **Description:** Implement the logic within `process_document_for_mvp` task:
        1.  Update `Document` status to "PROCESSING" in PostgreSQL.
        2.  Extract text from PDF at `file_path` (P4-T2).
        3.  Chunk the extracted text (P4-T3).
        4.  For each chunk:
            a.  Generate a unique ID for the chunk (e.g., UUID).
            b.  Create `DocumentChunk` node in Neo4j (P3-T5) linking to `document_id_pg` and storing `text` and `chunk_seq_num`.
            c.  Get embedding for the chunk's text (P4-T5).
            d.  Add embedding to Vector DB (P3-T7) with metadata: `chunk_id` (Neo4j node ID or the UUID), `document_id_pg`.
        5.  Update `Document` status to "COMPLETED" in PostgreSQL. Handle errors by setting status to "FAILED".
    * **Start State:** Task is empty.
    * **End State:** Task performs all steps.
    * **Test:** (Integration Test) Upload a PDF. Manually trigger the Celery task (or modify upload endpoint to call it synchronously for now for easier testing). Verify:
        * `Document` status updated in PostgreSQL.
        * `DocumentChunk` nodes created in Neo4j with correct text and relations.
        * Embeddings and metadata stored in Vector DB.

* **Task ID: P4-T8**
    * **Description:** Modify `/documents/upload` endpoint to asynchronously call `process_document_for_mvp.delay(...)` after creating the "PENDING" document record.
    * **Start State:** Upload endpoint does not trigger processing.
    * **End State:** Upload endpoint now dispatches the Celery task.
    * **Test:** Upload a PDF. Observe Celery worker logs to see the task being picked up and executed. Verify DB changes as in P4-T7.

* **Task ID: P4-T9**
    * **Description:** Create a `/documents/{document_id_pg}/query` POST endpoint (`app/api/v1/documents.py`).
    * **Start State:** No way to query a document.
    * **End State:** Endpoint definition exists but is not implemented.
    * **Test:** N/A (definition only).

* **Task ID: P4-T10**
    * **Description:** Implement the logic for `/documents/{document_id_pg}/query` (Basic RAG - Step 1: Retrieval):
        1.  Requires authenticated user.
        2.  Accepts a JSON body like `{"question": "user's question"}`.
        3.  Get embedding for the user's question (P4-T5).
        4.  Query Vector DB (P3-T7) for top K similar chunks, filtering by `document_id_pg` (from path parameter).
        5.  For this MVP, return the raw text of the retrieved chunks directly in the JSON response. Example: `{"retrieved_chunks": [{"text": "chunk1_text"}, {"text": "chunk2_text"}]}`.
    * **Start State:** Endpoint is not implemented.
    * **End State:** Endpoint retrieves and returns relevant text chunks.
    * **Test:** Upload and process a document. Call this endpoint with a question relevant to the document. Verify the response contains text chunks that are indeed relevant.

---

### Phase 5: Simplest Frontend for Testing Core Flow (Extremely Minimal)

*Note: These are minimal tasks, assuming an engineering LLM might generate basic HTML/JS or you'll use Postman extensively. If a human is building this, they'd likely use a framework from the start.*

* **Task ID: P5-T1**
    * **Description:** Create a basic HTML page (`frontend_test/index.html`) with forms for user registration and login.
    * **Start State:** No frontend.
    * **End State:** HTML page with forms. JS to submit form data to backend `/users/` and `/login/access-token` endpoints and store/display JWT.
    * **Test:** Register a user. Log in. See JWT displayed.

* **Task ID: P5-T2**
    * **Description:** Add a file upload form to `index.html` that submits to `/documents/upload` (sending JWT in header).
    * **Start State:** Login works. No upload UI.
    * **End State:** User can upload a PDF after logging in. Display document ID and status from response.
    * **Test:** Log in, upload a PDF. Check network tab for successful request/response. Check backend logs/DBs for processing.

* **Task ID: P5-T3**
    * **Description:** Add a form to `index.html` to query an uploaded document. Input fields for `document_id_pg` and `question`.
    * **Start State:** Upload works. No query UI.
    * **End State:** User can input document ID and question, JS submits to `/documents/{document_id_pg}/query` (sending JWT). Display raw retrieved chunk texts.
    * **Test:** After uploading and processing a document, use its ID to ask a question. See relevant text chunks displayed.

---

### Phase 6: Introduce LLM for Basic Summarization/Answering (Simplest LangGraph Element)

* **Task ID: P6-T1**
    * **Description:** Create a function in `app/services/llm_service.py` for basic question answering given context.
    * **Start State:** `llm_service.py` only has embedding function.
    * **End State:** `answer_question_with_context(question: str, context_chunks: List[str])` function:
        1.  Constructs a prompt: "Given the following context: [concatenated text of context_chunks]. Answer the question: [question]".
        2.  Calls OpenAI completions/chat API.
        3.  Returns the LLM's textual answer.
    * **Test:** Unit test: call with a sample question and context, verify an answer string is returned.

* **Task ID: P6-T2**
    * **Description:** Modify the `/documents/{document_id_pg}/query` endpoint (P4-T10) logic:
        1.  After retrieving top K similar chunks from Vector DB.
        2.  Instead of returning raw chunks, pass the question and the text of these chunks to `answer_question_with_context` (P6-T1).
        3.  Return the LLM's answer in the JSON response. Example: `{"answer": "llm_generated_answer", "retrieved_chunks": [...]}` (still good to return chunks for traceability).
    * **Start State:** Endpoint returns raw chunks.
    * **End State:** Endpoint returns an LLM-generated answer based on retrieved chunks.
    * **Test:** Using the frontend test page (or Postman), ask a question to a processed document. Verify the answer is coherent and based on the document's content. Compare with just raw chunk retrieval.

---

This MVP plan is highly sequential and foundational, building up the system piece by piece. Each step should be small enough for an engineering LLM to tackle and for you to test effectively. Good luck!