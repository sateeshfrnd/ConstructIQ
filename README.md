# 🏗️ ConstructIQ

A construction expense management system built for tracking building material costs, labor, contracts, and site expenses across different construction stages. Designed for individual home builders to monitor every rupee spent — from foundation to finishing.

## Features

### 📊 Dashboard
- Total project cost at a glance
- Category-wise expense breakdown with charts
- Stage-wise spend (Foundation, Structure, Plastering, Finishing)
- Payment mode distribution (Cash / UPI / Bank Transfer)
- Materials vs Workforce vs Other expense split with progress indicators

### 🧱 Material Tracking
| Category | Metrics Tracked |
|----------|----------------|
| **Cement** | Total bags, spend, paid, outstanding |
| **Steel** | Bundles, weight (KG), cost by TMT size, binding wire |
| **Bricks** | Quantity by size (4-inch/6-inch), cost per size |
| **Sand** | Loads by type (Double/Single Washed), cost per type |
| **Stone** | Loads by type (20mm/40mm/Rocks), cost per type |

### 👷 Workforce Tracking
| Category | Metrics Tracked |
|----------|----------------|
| **Labour** | Total paid, breakdown by type (Civil, Steel Bending, Concrete) |
| **Electrical** | Spend by category (Wiring, Fittings, Temporary EB, Labor) |
| **Plumbing** | Spend by category (Pipes, Fittings, Sanitary, Labor) |
| **Painting** | Spend by category (Paint, Primer, Putty, Labor) |

### 📋 Civil Contract Management
- Contract setup with auto-calculated chadaras and total cost
- Payment tracking with stage-wise history
- Expected vs Actual comparison per construction stage
- Progress bar showing overall payment percentage
- Support for structure, plastering, and additional work stages

### 📦 Site / Miscellaneous Expenses
- Architect Fee, Excavation, Readymix Concrete, Loan Process, etc.
- Category-wise breakdown with entry count and cost

### 📤 Bulk Load
- Upload CSV or Excel files to bulk-import historical data
- Schema validation with clear error messages
- Data preview before committing to database
- Supports all 10 expense categories

### ✏️ Edit / Delete Entries
- Select any entry from history to edit or delete
- Inline edit form with all fields pre-filled
- Works across all categories

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose) + bcrypt |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
ConstructIQ/
├── backend/
│   ├── core/              # Security (JWT, password hashing)
│   ├── database/          # SQLAlchemy engine and session
│   ├── models/            # ORM models (one per expense type)
│   ├── schemas/           # Pydantic request/response models
│   ├── routers/           # FastAPI route handlers
│   ├── services/          # Business logic and DB queries
│   ├── repositories/      # User repository
│   ├── utils/             # Constants (table names)
│   ├── main.py            # FastAPI app entry point
│   ├── create_user.py     # Admin user seeder
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── components/        # Reusable UI (sidebar, metric cards, editable table)
│   ├── page_layouts/      # One file per page/feature
│   ├── services/          # API client (HTTP calls to backend)
│   ├── assets/            # CSS styles
│   ├── utils/             # Frontend constants
│   ├── app.py             # Streamlit app entry point
│   ├── Dockerfile
│   └── requirements.txt
├── sample_data/           # CSV files for bulk load testing
├── docker-compose.yml
├── DOCKER.md              # Docker setup and commands
├── pyproject.toml
└── README.md
```

---

## Quick Start (Docker)

```bash
# Build and start all services
docker-compose up --build

# Seed admin user (first time only)
docker exec -it constructiq-backend python create_user.py
```

Open:
- **App**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Login**: `admin@example.com` / `admin710`

See [DOCKER.md](DOCKER.md) for full Docker reference (logs, backup, troubleshooting).

---

## Quick Start (Without Docker)

### Prerequisites
- Python 3.12+
- PostgreSQL running locally
- Create database: `construct_iq`

### Backend

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:pass@localhost:5432/construct_iq"
uvicorn main:app --reload --port 8000

# Seed admin user
python create_user.py
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## API Endpoints

### Auth
- `POST /auth/login` — Login with email/password, returns JWT

### Expenses (per category)
- `POST /{category}/` — Add new entry
- `GET /{category}/` — List all entries
- `GET /{category}/metrics` — Aggregated metrics with optional filters

### CRUD
- `PUT /entries/{category}/{id}` — Update an entry
- `DELETE /entries/{category}/{id}` — Delete an entry

### Bulk Load
- `GET /bulk_load/schema/{category}` — Get expected columns
- `POST /bulk_load/{category}` — Bulk insert records

### Civil Contract
- `POST /civil_contract/` — Create contract
- `GET /civil_contract/` — List contracts
- `POST /civil_contract/payments` — Add payment
- `GET /civil_contract/{id}/payments` — Get payments
- `POST /civil_contract/{id}/stages` — Save stage budget
- `GET /civil_contract/{id}/summary` — Full summary with expected vs actual

### Dashboard
- `GET /dashboard/summary` — Complete project overview

---

## Sample Data

The `sample_data/` directory contains CSV files for each category to test the bulk load feature:

```
sample_data/
├── cement_sample.csv
├── bricks_sample.csv
├── steel_sample.csv
├── sand_sample.csv
├── stone_sample.csv
├── labour_sample.csv
├── electric_sample.csv
├── plumbing_sample.csv
├── painting_sample.csv
└── site_expenses_sample.csv
```

---

## Default Credentials

| Field | Value |
|-------|-------|
| Email | admin@example.com |
| Password | admin710 |
| Role | admin |

---

## License

Private project. Not for redistribution.
