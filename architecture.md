## Product Requirements Document: AI Grant Writer (Project "Aura")

* **Version:** 1.1 (Enhanced Architecture Detail)
* **Date:** June 4, 2025
* **Author:** Gemini Assistant (in collaboration with user)
* **Status:** Draft

### 1. Introduction & Vision

#### 1.1. The Problem
Non-profit organizations, the backbone of social progress, depend on grant funding to operate and innovate. However, the process of finding and applying for grants is notoriously time-consuming, repetitive, and resource-intensive. Staff members, who are often overstretched, spend hundreds of hours each year manually searching for opportunities, gathering organizational information, and writing bespoke proposals for each application. This administrative burden detracts from their primary mission: serving their communities.

#### 1.2. The Vision
Project "Aura" will be an intelligent, conversational AI grant writer that acts as a collaborative partner for non-profits. It will centralize organizational knowledge, automate the tedious aspects of grant writing, and proactively identify funding opportunities. By transforming grant writing from a manual chore into an efficient, AI-assisted workflow, Aura will free up non-profits to focus on what they do best: creating impact.

#### 1.3. Core Value Proposition
Aura will empower non-profits to win more funding with less effort.

### 2. Target Audience

* **Primary User:** The Non-Profit Administrator. This could be an Executive Director, a dedicated Grant Manager, or a Program Manager at a small-to-medium-sized non-profit organization ($500k - $10M annual budget) who wears multiple hats and is not a professional grant writer. They are tech-savvy enough to use modern web applications but are not developers. They value accuracy, efficiency, and trust.

### 3. User Stories

#### 3.1. Knowledge Base Creation
* **As a** non-profit director, **I want to** upload a folder of my existing documents (annual reports, past grants, strategic plans), **so that** the AI can learn about my organization's history, mission, and projects without me having to re-type everything.
* **As a** program manager, **I want** the AI to ask me specific, clarifying questions about my projects, **so that** I can provide accurate details (like KPIs and budgets) that are often missing from general documents.
* **As a** user, **I want** to know that the information I provide is stored securely and can be easily updated, **so that** the AI's knowledge base remains current and trustworthy over time.

#### 3.2. Interactive Grant Writing
* **As a** grant manager, **I want to** upload a new grant application PDF, **so that** the system can automatically analyze it and identify all the questions I need to answer.
* **As a** grant manager, **I want** the AI to instantly fill out all the questions it already knows the answers to, **so that** I can immediately see how much work is left.
* **As a** grant manager, **I want** the AI to guide me through the remaining questions with a conversation, **so that** I can provide the missing information efficiently.
* **As a** user, **I want** to see the source of the information the AI uses (e.g., "from 2024 Annual Report, pg. 5"), **so that** I can verify the accuracy of the generated content.
* **As a** user, **I want** to review the final, generated grant draft and provide stylistic feedback (e.g., "make this section more concise"), **so that** the final output matches the funder's tone.

#### 3.3. Grant Discovery
* **As an** executive director, **I want** the system to automatically find and suggest new grant opportunities that my organization is a good fit for, **so that** I don't have to spend hours searching on my own.

### 4. Core Features & Functionality (V1)

#### 4.1. The Knowledge Base ("Corporate Brain")
* **F-KB-1: Multi-Format Document Ingestion:** Users can upload documents in `.pdf`, `.docx`, and `.txt` formats.
* **F-KB-2: Asynchronous Processing:** Document uploads will be processed in the background. The UI will immediately confirm the upload and notify the user upon completion (See T-ARC-7).
* **F-KB-3: Conversational Data Intake:** The AI will initiate a conversation to fill gaps in its knowledge, based on a predefined checklist of essential non-profit information (mission, history, key staff, main projects, etc.).
* **F-KB-4: Knowledge Update:** New information provided by the user in conversation is used to update the central knowledge graph.

#### 4.2. The Interactive Grant Writer
* **F-GW-1: Grant Application Parsing:** The system will accept an uploaded grant application (PDF) and intelligently extract all question fields and text areas.
* **F-GW-2: Automated First-Pass Fill:** The system will query the Knowledge Base and automatically answer all questions for which it has high-confidence data.
* **F-GW-3: Gap Analysis & Presentation:** The UI will clearly display which questions were answered automatically, which are partially answered, and which are empty.
* **F-GW-4: Conversational Gap-Filling:** The AI will guide the user through the empty questions in a conversational manner (See T-ARC-4).
* **F-GW-5: Source Citation:** All automatically generated answers must be accompanied by a citation pointing to the source document/information in the Knowledge Base.
* **F-GW-6: Draft Generation & Iteration:** Once all questions are answered, the system will generate a complete draft in a single document. Users can provide stylistic feedback for regeneration.
* **F-GW-7: Export:** The final draft can be downloaded as a `.docx` file.

#### 4.3. V1 Grant Discovery
* **F-GD-1: Profile Extraction:** The system will automatically create a structured profile of the user's organization from the Knowledge Graph (e.g., focus areas, geographic scope).
* **F-GD-2: Opportunity Matching:** The system will filter a database of grant opportunities against the organization's profile using tag-based matching.
* **F-GD-3: Opportunity Dashboard:** A simple dashboard will display a list of potential grant opportunities, with links to the original source.

### 5. Technical Architecture & Requirements (V1 Focus)

#### 5.1. Guiding Principles
* **Modularity:** Components should be loosely coupled to allow for independent development, testing, and scaling.
* **Scalability:** Design for growth in users, data volume, and processing load.
* **Accuracy & Verifiability:** Prioritize correct information retrieval and provide transparent sourcing.
* **Security:** Implement robust security measures to protect sensitive non-profit data.
* **Maintainability:** Write clean, well-documented code with comprehensive tests.

#### 5.2. System Overview Diagram

```
+----------------+     HTTPS/JSON      +----------------------+     +-----------------+
| User (Browser)|<------------------->|   Backend (FastAPI)  |<--->|   LLM Provider  |
|   (Frontend)  |                     |  (Orchestration via  |     |    (OpenAI API) |
+----------------+                     |      LangGraph)      |     +-----------------+
                                      +----------------------+
                                         ^   |         ^   |
                                         |   |         |   |
                                         |   v         |   v
        +-----------------------------+  |   |         |  +----------------------------+
        |    Celery Task Queue        |<---- |         ---->| PostgreSQL (User, App Meta)|
        | (Redis/RabbitMQ for Broker) |  |   |         |  +----------------------------+
        +-----------------------------+  |   |         |
          |         ^                    |   |         |
          v         |                    |   v         |
+---------------------+                  |  +---------------------+
| Celery Worker(s)    |<------------------  |  Neo4j (Graph DB)   |
| (Document Proc.,  |                     |  + Vector Index     |
|  AI Background Task)|                     +---------------------+
+---------------------+
```

#### 5.3. Component Breakdown & Responsibilities

##### 5.3.1. Frontend
* **Technology:** Modern JavaScript Framework (e.g., React with TypeScript, Vite for build). State management library (e.g., Zustand, Redux Toolkit). UI component library (e.g., Material UI, Tailwind CSS).
* **Responsibilities:**
    * Render user interface for all features (document upload, chat, grant review, dashboard).
    * Handle user input and interactions.
    * Manage client-side state (e.g., current view, form data, UI elements).
    * Communicate with the Backend API via HTTPS/JSON (RESTful principles).
    * Display notifications for asynchronous tasks (e.g., document processing status via WebSockets or polling).
* **Conceptual File/Folder Structure (Example - React):**
    ```
    aura-frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── assets/            # Static assets like images, fonts
    │   ├── components/        # Reusable UI components (Button, Modal, ChatBubble)
    │   │   ├── common/
    │   │   └── features/      # Feature-specific components
    │   ├── features/          # Feature-specific views and logic
    │   │   ├── auth/
    │   │   ├── knowledge_base/
    │   │   ├── grant_writing/
    │   │   └── grant_discovery/
    │   ├── services/          # API communication layer (e.g., api.js)
    │   ├── store/             # State management (e.g., Zustand stores)
    │   ├── hooks/             # Custom React hooks
    │   ├── utils/             # Utility functions
    │   ├── App.tsx            # Main application component
    │   └── main.tsx           # Entry point
    ├── package.json
    └── tsconfig.json
    ```
* **State Management:**
    * Local component state for UI elements.
    * Global state (Zustand/Redux) for user authentication, active grant session, and application-wide notifications.
* **API Communication:** Primarily RESTful HTTP requests to the backend. Authentication via JWT tokens sent in Authorization headers.

##### 5.3.2. Backend (API Server)
* **Technology:** Python 3.10+ with FastAPI. Pydantic for data validation.
* **Responsibilities:**
    * Expose RESTful API endpoints for frontend interaction.
    * Handle user authentication and authorization.
    * Orchestrate business logic using the LangGraph engine for grant writing workflows.
    * Interact with databases (PostgreSQL, Neo4j, Vector DB).
    * Delegate long-running tasks (e.g., document ingestion) to the Celery task queue.
    * Manage API keys and secure communication with external services (LLM provider).
* **Conceptual File/Folder Structure (Example - FastAPI):**
    ```
    aura-backend/
    ├── app/
    │   ├── api/                # API Routers (endpoints)
    │   │   ├── v1/
    │   │   │   ├── auth.py
    │   │   │   ├── documents.py
    │   │   │   ├── grant_sessions.py
    │   │   │   └── users.py
    │   ├── core/               # Core logic, configuration, security
    │   │   ├── config.py
    │   │   └── security.py
    │   ├── crud/               # Create, Read, Update, Delete operations for databases
    │   │   ├── crud_user.py
    │   │   └── crud_document.py
    │   ├── db/                 # Database session management, models (SQLModel/SQLAlchemy)
    │   │   ├── base.py
    │   │   ├── session.py
    │   │   └── models_pg.py    # PostgreSQL models
    │   ├── schemas/            # Pydantic schemas for request/response validation
    │   │   ├── user_schemas.py
    │   │   └── grant_schemas.py
    │   ├── services/           # Business logic services
    │   │   ├── knowledge_graph_service.py # Interacts with Neo4j
    │   │   ├── llm_service.py             # Interface to LLM provider
    │   │   └── grant_processing_service.py # Orchestrates grant writing via LangGraph
    │   ├── langgraph_flows/    # LangGraph definitions
    │   │   ├── grant_writer_graph.py
    │   │   └── state_models.py
    │   ├── tasks/              # Celery task definitions (e.g., process_document.py)
    │   ├── main.py             # FastAPI application instance and startup events
    │   └── worker.py           # Celery worker startup script
    ├── tests/                  # Unit and integration tests
    ├── .env                    # Environment variables
    ├── requirements.txt
    └── Dockerfile
    ```
* **Authentication & Authorization:** JWT-based authentication. Endpoints will be protected, requiring valid tokens.

##### 5.3.3. Orchestration Layer (LangGraph Engine)
* **Role:** Lives within the Backend (`aura-backend/app/langgraph_flows/` and `aura-backend/app/services/grant_processing_service.py`). It is the core engine for the interactive grant writing workflow.
* **LangGraph `State` Object:** A Pydantic model representing the current state of a grant writing session. Passed between nodes. Persisted (e.g., in Redis or PostgreSQL) if a session needs to be resumable across long periods.
    * **Contents (Example):**
        ```python
        class GrantWriterState(TypedDict):
            user_id: str
            grant_application_id: str # ID of the uploaded grant doc
            original_grant_doc_path: str
            structured_questions: List[Dict] # {"id": int, "question_text": str, "answer_text": Optional[str], "source_citation": Optional[str], "status": Literal["answered", "partial", "unanswered"]}
            current_question_index: int
            conversation_history: List[Dict] # {"speaker": "ai" | "user", "content": str}
            knowledge_graph_query_attempts: Dict[int, int] # question_id: attempt_count
            user_feedback_on_draft: Optional[str]
            final_draft_path: Optional[str]
        ```
* **LangGraph Nodes & Edges:** Defined in `grant_writer_graph.py`.
    1.  **`initialize_session`**: Loads grant application, user ID.
    2.  **`parse_grant_application`**: Extracts text from the PDF, uses an LLM to structure questions into `structured_questions` in the State.
    3.  **`query_knowledge_graph`**: (Iterates through `structured_questions` with status "unanswered")
        * For each question, calls `llm_service.py` to generate a Cypher query (Text2Cypher, providing graph schema).
        * Executes query via `knowledge_graph_service.py` against Neo4j.
        * If answer found, updates question status and `answer_text`, `source_citation` in State.
    4.  **`check_completion_status` (Conditional Edge)**:
        * If all questions "answered" -> go to `generate_initial_draft`.
        * Else -> go to `formulate_user_prompt`.
    5.  **`formulate_user_prompt`**: Identifies unanswered questions, uses LLM to create a single, consolidated, conversational prompt for the user. Appends to `conversation_history`.
    6.  **(User Input via API)**: Frontend sends user's response. Backend updates `conversation_history`.
    7.  **`update_knowledge_graph`**: LLM parses user's response. Generates Cypher statements to `MERGE`/`CREATE` new data/relationships in Neo4j via `knowledge_graph_service.py`.
    8.  **(Loop Edge)**: Go back to `query_knowledge_graph` to try answering with new info.
    9.  **`generate_initial_draft`**: LLM uses all `structured_questions` (with answers) to generate a coherent draft. Updates State.
    10. **`handle_user_feedback_on_draft` (Conditional Edge)**:
        * If user provides feedback -> update `user_feedback_on_draft` in State, go to `regenerate_draft_with_feedback`.
        * Else (user approves) -> go to `finalize_session`.
    11. **`regenerate_draft_with_feedback`**: LLM uses initial draft and `user_feedback_on_draft` to refine. Updates State.
    12. **`finalize_session`**: Marks session complete.

##### 5.3.4. LLM Interface Module (`aura-backend/app/services/llm_service.py`)
* **Responsibilities:**
    * Abstracts all direct calls to the LLM provider (OpenAI).
    * Manages API key securely (from `config.py`).
    * Contains well-defined functions for specific tasks (e.g., `get_llm_completion`, `generate_cypher_query_from_question`, `parse_text_to_structured_questions`, `generate_grant_narrative`).
    * Handles prompt templating and management.
    * Implements retry logic and error handling for LLM API calls.

##### 5.3.5. Databases
* **Neo4j (Graph Database):**
    * **Role:** Stores the structured "Corporate Brain" – entities (projects, staff, KPIs, etc.) and their relationships. Also stores embeddings for textual properties of nodes for hybrid search.
    * **Schema:** Defined in T-ARC-4 of the previous PRD version (e.g., `Organization`, `Project` nodes). Properties like `Project.description_embedding` will store vectors.
    * **Connection:** Python driver (e.g., `neo4j-driver`) from `knowledge_graph_service.py`. Connection details from `config.py`.
    * **Query Generation:** Primarily via Text2Cypher LLM calls managed in `llm_service.py`, passing the graph schema for context.
* **Vector Database (or Neo4j's native vector index):**
    * **Role:** Stores vector embeddings of text chunks (from documents, project descriptions, etc.) for fast semantic similarity searches.
    * **Connection:** Python client for the chosen vector DB, or via Neo4j driver if using its native index.
    * **Relationship to Neo4j:** Chunks stored in the vector DB will have metadata linking them back to their parent node ID in Neo4j (e.g., `Project_ID_123`, `document_chunk_hash`). This enables hybrid search: find relevant nodes via vector search, then traverse graph for structured info.
* **PostgreSQL (Relational Database):**
    * **Role:** Stores user accounts (hashed passwords, profiles), application metadata (e.g., uploaded document records, grant writing session state IDs if persisted), Celery task metadata, and V1 grant discovery opportunities.
    * **Connection:** SQLAlchemy/SQLModel with Alembic for migrations. Session management in `db/session.py`.

##### 5.3.6. Asynchronous Task Processing (Celery & Redis/RabbitMQ)
* **Responsibilities:** Handles long-running, resource-intensive tasks that should not block the API server.
    * Primary use case: Document ingestion pipeline (F-KB-2).
    * Potential future use: Batch report generation, large-scale knowledge graph updates.
* **Task Definition (`aura-backend/app/tasks/`):** Python functions decorated with `@celery.task`.
    * Example: `process_document_task(document_id: int, file_path: str)`
* **State:** Task state (PENDING, STARTED, SUCCESS, FAILURE) is managed by Celery and can be stored in the Celery backend (e.g., Redis or PostgreSQL).
* **Communication Flow:**
    1.  Backend API receives a request (e.g., document upload).
    2.  API endpoint creates a record in PostgreSQL (e.g., `DocumentUploads` table with status "PENDING") and then calls `.delay()` or `.apply_async()` on a Celery task, passing relevant IDs/data.
    3.  Celery worker picks up the task from the broker (Redis/RabbitMQ).
    4.  Worker executes the task (e.g., document parsing, chunking, embedding, Neo4j ingestion).
    5.  Worker updates the PostgreSQL record (e.g., status "COMPLETED" or "FAILED", and stores paths to processed data).
    6.  Frontend can poll an API endpoint for task status or receive updates via WebSockets.

##### 5.3.7. Document Intelligence Pipeline (within Celery tasks)
* **Tools:** Libraries like `PyMuPDF` (for PDF text/image extraction), `python-docx` (for DOCX), `unstructured.io` (for complex layout parsing and chunking).
* **Responsibilities:**
    1.  **Parsing:** Extract raw text and identify structural elements (headings, paragraphs, tables, lists) from various document formats.
    2.  **Chunking:** Divide extracted text into meaningful, semantically coherent chunks suitable for embedding. Strategy: Aim for ~paragraph-sized chunks, respecting document structure. Store metadata with each chunk (source document ID, page, chunk sequence).
    3.  **Embedding:** Use an embedding model (e.g., via OpenAI's API or a local sentence-transformer model) to convert text chunks into vector embeddings.
    4.  **Entity/Relationship Extraction (Advanced V2):** Potentially use LLMs to identify key entities and relationships within chunks to suggest additions to the graph.
    5.  **Loading:** Store text chunks and their embeddings in the Vector DB (or Neo4j vector index) and link them to conceptual nodes created/updated in Neo4j.

#### 5.4. Data Flow Examples

##### 5.4.1. User Document Upload & Ingestion Flow
1.  **Frontend:** User selects file(s) and clicks "Upload." JS sends a multipart/form-data POST request to `/api/v1/documents/upload`.
2.  **Backend API (`documents.py`):**
    * Authenticates user.
    * Saves file(s) to temporary storage.
    * Creates a `Document` record in PostgreSQL with status "PENDING" and user association.
    * Dispatches `process_document_task(document_id, temp_file_path)` to Celery.
    * Returns `202 ACCEPTED` to Frontend with the `document_id`.
3.  **Frontend:** Displays "Processing document..." for the given `document_id`. Polls `/api/v1/documents/{document_id}/status` or listens on WebSocket.
4.  **Celery Worker (`process_document.py`):**
    * Retrieves `document_id` and `temp_file_path`.
    * Updates `Document` status to "PROCESSING".
    * **Document Intelligence Pipeline:** Parses file, chunks text, generates embeddings.
    * **Neo4j/Vector DB Update:** Loads chunks/embeddings into Vector DB, creates/updates related nodes and relationships in Neo4j (e.g., `ReportDocument` node, links to `Project` nodes if mentioned).
    * Updates `Document` status to "COMPLETED" or "FAILED". Cleans up temp file.
5.  **Frontend:** Receives status update and reflects it in the UI.

##### 5.4.2. Interactive Grant Application Filling Flow (Simplified)
1.  **Frontend:** User uploads grant PDF to `/api/v1/grant_sessions/start`.
2.  **Backend API (`grant_sessions.py`):**
    * Initializes a new LangGraph session (via `grant_processing_service.py`). The initial `GrantWriterState` is created.
    * The `parse_grant_application` node in LangGraph is invoked. It uses `llm_service.py` to process the PDF into `structured_questions` in the State.
    * The LangGraph instance (or its state ID) is associated with the user's session.
    * Returns initial state (e.g., list of questions) to Frontend.
3.  **LangGraph Engine (executing `query_knowledge_graph` node):**
    * For each question, `llm_service.py` generates a Cypher query.
    * `knowledge_graph_service.py` executes query against Neo4j.
    * Answers are populated in the `GrantWriterState`.
4.  **Frontend:** Displays questions, pre-filled answers, and citations.
5.  **LangGraph Engine (executing `formulate_user_prompt` node if gaps exist):**
    * `llm_service.py` creates a conversational prompt for missing info.
    * Backend API sends this prompt to Frontend via a `/api/v1/grant_sessions/{session_id}/chat` endpoint (could be long-polling or WebSocket).
6.  **Frontend:** User types response and POSTs to `/api/v1/grant_sessions/{session_id}/chat`.
7.  **Backend API/LangGraph Engine:**
    * Adds user message to `conversation_history` in `GrantWriterState`.
    * Invokes `update_knowledge_graph` node: `llm_service.py` parses user's response; `knowledge_graph_service.py` updates Neo4j.
    * LangGraph loops back to `query_knowledge_graph` to try filling more questions.
8.  This cycle repeats until `check_completion_status` routes to `generate_initial_draft`.
9.  **LangGraph Engine (`generate_initial_draft` node):**
    * `llm_service.py` generates draft from all answered questions.
    * Draft is sent to Frontend.
10. **Frontend:** User reviews, optionally provides feedback (POSTs to `/api/v1/grant_sessions/{session_id}/feedback`).
11. **LangGraph Engine (`regenerate_draft_with_feedback` if feedback given):**
    * `llm_service.py` refines draft.
    * Updated draft sent to Frontend.
12. **Frontend:** User downloads final draft. Session can be marked as finalized.

#### 5.5. Security Considerations (V1)
* **Authentication:** JWT for API authentication. Secure password hashing (e.g., bcrypt).
* **Authorization:** Ensure users can only access and modify their own data.
* **Data Encryption:**
    * HTTPS/TLS for all client-server communication.
    * Encryption at rest for databases (standard feature for most managed DB services).
    * Securely manage API keys and secrets (e.g., HashiCorp Vault, or environment variables in a secure hosting environment).
* **Input Validation:** Rigorous Pydantic validation for all API inputs to prevent injection attacks.
* **Dependency Management:** Regularly scan and update dependencies to patch vulnerabilities.
* **Rate Limiting:** Implement rate limiting on sensitive API endpoints to prevent abuse.

### 6. V1 Scope: In & Out

| In Scope (V1)                                                              | Out of Scope (For now)                                                     |
| :------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| English language only.                                                     | Multi-language support.                                                    |
| Document uploads: `.pdf`, `.docx`, `.txt`.                                 | Image files, spreadsheets, or other formats.                               |
| Grant Discovery via scraping Grants.gov.                                   | Integration with paid grant database APIs (e.g., Instrumentl).             |
| Exporting final draft as `.docx`.                                          | Direct submission to grant portals.                                        |
| User authentication (email/password).                                      | SSO / Google authentication.                                               |
| Handling ambiguity by asking the user for clarification.                   | Fully autonomous disambiguation.                                           |
| Individual user accounts.                                                  | Multi-user team accounts with roles and permissions.                       |
| Basic PDF text extraction; table extraction is best-effort for V1.         | Advanced table/image understanding beyond simple text extraction.          |

### 7. Success Metrics
* **Activation & Engagement:**
    * Number of active non-profit organizations.
    * Average number of documents uploaded per organization.
* **Core Functionality:**
    * Average percentage of grant application questions auto-filled on the first pass.
    * Average time (in hours) saved per grant application (measured via user survey).
* **User Satisfaction:**
    * Net Promoter Score (NPS) or Customer Satisfaction (CSAT) score.
    * Qualitative feedback on the trust and accuracy of the generated content.
    * Task completion rate for key workflows.

### 8. Open Questions & Future Considerations
* **Scalability of LLM Calls:** How to manage costs and latency for LLM-intensive tasks like Text2Cypher and text generation for many users?
* **Accuracy of Text2Cypher:** What level of accuracy can be reliably achieved? How much human oversight or schema refinement is needed?
* **Long-Term State Management for LangGraph:** For very long, multi-day grant writing sessions, how should the LangGraph `State` object be persisted and resumed efficiently? (Redis, PostgreSQL JSONB field, etc.)
* **User Onboarding & Education:** How to best guide users to provide the *right* initial documents for optimal Knowledge Base creation?
* **Future Features:**
    * **Predictive Analytics:** Analyze funder data to predict the likelihood of success for a given application.
    * **Budget Builder:** An interactive tool to help users create project budgets from scratch.
    * **Direct Portal Integration:** Use browser automation to fill out online grant application forms directly.
    * **Team Collaboration:** Allow multiple users from one organization to collaborate on a single application.
    * **Advanced Document Intelligence:** Deeper understanding of tables, charts, and images within documents.