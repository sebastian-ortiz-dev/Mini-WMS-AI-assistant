# Mini WMS & AI Assistant Backend

A backend service for a Warehouse Management System (WMS) built with **FastAPI**, **PostgreSQL**, and an integrated **AI Agent** for natural language inventory operations and read-only database queries.

---

## Architectural Decisions & Core Solutions

To satisfy the core requirements of this assessment, several key architectural decisions were implemented:

### 1. Safe Picking, Concurrency Control & Database Constraints (Preventing Overselling & Negative Stock)
- **The Challenge:** Multiple users attempting to pick the same inventory item simultaneously can lead to race conditions, stale reads, and negative stock balances.
- **The Solution:** 
  - **Row-Level Locking:** The backend uses PostgreSQL transactional isolation combined with row-level locking (`SELECT ... FOR UPDATE`) during picking operations to explicitly serialize concurrent requests without locking entire tables.
  - **Database-Level Constraints:** Physical `CHECK` constraints (e.g., `CHECK (quantity >= 0)`) are embedded directly into the database schema. This acts as an absolute safety net, making it structurally impossible for the database to accept or persist negative inventory values, regardless of application-level edge cases.

### 2. Full Movement History & Audit Trail
- Every stock operation (receiving, moving, picking, and shipping) writes an immutable event log to a movement history table.
- The audit trail captures **who** performed the action (via JWT claims), **what** items and quantities were affected, **when** it occurred (`TIMESTAMPTZ`), and the precise **origin and destination bins**.

### 3. Read-Only AI Assistant Guardrails & Least Privilege Security
- **The Challenge:** Exposing an LLM to database operations risks destructive queries or prompt injections attempting to modify or drop data.
- **The Solution:** The AI assistant (powered by Google Gemini) operates under a rigorous defense-in-depth security model:
  1. **Dedicated Low-Privilege Database Role:** A separate PostgreSQL user role is explicitly created for the AI agent with only `SELECT` privileges granted. 
  2. **Database Engine Enforcement:** Even if a prompt injection tricks the model into generating an `UPDATE`, `DELETE`, or `DROP` statement, the PostgreSQL database engine itself rejects it instantly at the driver level due to permission restrictions.
  3. **Scoped Introspection:** The assistant is programmatically restricted to generating safe, read-only analytical queries for inventory levels and open orders.

⚠️ **Important Note on AI Integration:** 
To run the AI Assistant features, you must configure your own **Google API Key** in your `.env` file (`GOOGLE_API_KEY=your_key_here`). It is strongly recommended to configure the model to use **`gemini-3.5-flash-lite`** to fully leverage the free tier quotas during evaluation.

---

## Tech Stack

* **Framework:** FastAPI (Python) with Pydantic for request/response validation.
* **Database & Driver:** PostgreSQL, managed via raw SQL and `psycopg2` for explicit query control and high execution performance.
* **Testing:** Pytest with **Testcontainers** for ephemeral, isolated PostgreSQL containers on every test run.
* **AI SDK:** Google Gemini SDK (`google.genai`) for natural language database querying.
* **Security:** JWT-based authentication and secure cookie handling.

---

## Project Structure

```text
mini_WMS/
├── db/
│   ├── seed.sql             # Initial database seeders
│   └── wms_db.sql           # Database schema definition
├── src/
│   ├── middleware/          # Custom middlewares (auth, CORS, error handling)
│   ├── models/              # Pydantic validation schemas and DTOs
│   ├── repository/          # Direct SQL queries and database interaction layer
│   ├── secure/              # Security, JWT encoding/decoding, and hashing utils
│   ├── services/            # Core WMS business logic and AI agent integration
│   ├── static/              # Static files and assets
│   └── main.py              # FastAPI application entrypoint and route registration
├── tests/
│   └── integration/         # Integration test suite (Testcontainers + Pytest)
├── .env.example             # Environment variables template
├── pyproject.toml           # Project dependencies and tool configurations
├── uv.lock                  # Fast dependency lockfile (uv)
└── README.md                # Project documentation
```

---

## Core API Endpoints

1. Orders Management (/api/v1/orders)

* **POST/create:** Creates a new warehouse order, validating SKUs, bin existence, and sufficient inventory.

* **POST/{id_external}/pick:** Advances the order to the picking stage using concurrency-safe row locking.

* **POST/{id_external}/ship:** Finalizes order fulfillment and logs movement history.

2. Inventory & Warehouse

* Manages pallet receiving, bin-to-bin stock transfers, and real-time inventory tracking.

3. AI Assistant

* Natural language endpoint for stock levels, bin locations, and open order analysis.

---

## Getting Started & Installation
1. Prerequisites

* Python 3.10+

* Docker Desktop running (required for Testcontainers and local PostgreSQL instances).

2. Clone and Setup Virtual Environment

```bash
git clone https://github.com/sebastian-ortiz-dev/Mini-WMS-AI-assistant.git
cd Mini-WMS-AI-assistant
```

3. Configure Environment Variables
Copy the template file and configure your local environment settings (Database credentials, JWT secret keys, and Gemini API key):
```bash
cp .env.example .env
```

4. Install Dependencies

Using uv (Recommended):

```Bash
# Create and activate virtual environment
uv venv
# On Windows (PowerShell): .venv\Scripts\Activate
# On macOS/Linux: source .venv/bin/activate

# Sync dependencies from lockfile
uv sync
```

Or using standard pip:

```Bash
python -m venv .venv
# Activate virtual environment:
# On Windows (PowerShell): .venv\Scripts\Activate
# On macOS/Linux: source .venv/bin/activate
   
pip install -r requirements.txt
```

---

## Database Setup & Initialization

If you are running the application locally against a persistent PostgreSQL instance (note that integration tests automatically spin up ephemeral containers via Testcontainers), you can initialize the schema and seed data manually using the files in your `db/` folder:

1. **Create the Database:**
   ```bash
   psql -U postgres -c "CREATE DATABASE wms_db;"

Apply Schema and Seed Data:

```Bash
psql -U postgres -d wms_db -f db/wms_db.sql
psql -U postgres -d wms_db -f db/seed.sql
```

---

## Running Tests
The test suite uses Testcontainers to dynamically launch an isolated, real PostgreSQL database container on the fly, applying seeders automatically for a clean execution state.

To run the complete integration test suite with verbose output:

```Bash
$env:PYTHONPATH="."
pytest -v
```

---

## Running the Application
Start the local FastAPI development server:

```Bash
cd src

uv run fastapi dev
```

* Once running, access the interactive API documentation at:

Swagger UI: http://localhost:8000/docs
