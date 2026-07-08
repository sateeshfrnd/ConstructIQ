# ConstructIQ — Docker Setup Guide

Run the complete ConstructIQ application locally using Docker containers.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed (included with Docker Desktop)

## Services

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| PostgreSQL 16 | `constructiq-db` | 5432 | Database |
| FastAPI | `constructiq-backend` | 8000 | REST API |
| Streamlit | `constructiq-frontend` | 8501 | Web UI |

---

## Quick Start

```bash
# 1. Build and start all services
docker-compose up --build

# 2. (First time only) Seed the admin user
docker exec -it constructiq-backend python create_user.py
```

Open in browser:
- **App**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Login**: `admin@example.com` / `admin710`

---

## Common Commands

### Start / Stop

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached)
docker-compose up -d

# Stop all containers
docker-compose down

# Stop and remove database volume (fresh start)
docker-compose down -v
```

### Rebuild

```bash
# Rebuild after changing Dockerfile or requirements
docker-compose up --build

# Rebuild a specific service
docker-compose build backend
docker-compose build frontend
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Restart a Single Service

```bash
docker-compose restart backend
docker-compose restart frontend
```

---

## Database

### Connect to PostgreSQL

```bash
# Via psql inside the container
docker exec -it constructiq-db psql -U constructiq -d construct_iq

# From host (if psql installed locally)
psql -h localhost -p 5432 -U constructiq -d construct_iq
```

### Backup Database

```bash
docker exec -it constructiq-db pg_dump -U constructiq construct_iq > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker exec -i constructiq-db psql -U constructiq -d construct_iq
```

### Reset Database (delete all data)

```bash
docker-compose down -v
docker-compose up -d
docker exec -it constructiq-backend python create_user.py
```

---

## Development Workflow

Code changes are **hot-reloaded** automatically:
- Backend (FastAPI) — uvicorn watches for file changes
- Frontend (Streamlit) — auto-refreshes on save

No need to rebuild containers when editing Python files. Only rebuild when:
- Adding new packages to `requirements.txt`
- Modifying `Dockerfile`
- Changing `docker-compose.yml`

---

## Environment Variables

Copy `.env.example` to `.env` for custom configuration:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://constructiq:constructiq@db:5432/construct_iq` | PostgreSQL connection string |
| `SQL_ECHO` | `false` | Set `true` to log all SQL queries |
| `SECRET_KEY` | `constructiq-secret-key...` | JWT signing key |
| `API_BASE_URL` | `http://backend:8000` | Backend URL (from frontend container) |

---

## Troubleshooting

### Backend can't connect to database
```bash
# Check if DB is healthy
docker-compose ps

# Restart with fresh state
docker-compose down
docker-compose up -d
```

### Port already in use
```bash
# Check what's using the port
lsof -i :8000   # backend
lsof -i :8501   # frontend
lsof -i :5432   # postgres

# Kill the process or change ports in docker-compose.yml
```

### Permission denied on volumes
```bash
# Fix ownership
sudo chown -R $USER:$USER ./backend ./frontend
```

### Fresh start (nuclear option)
```bash
docker-compose down -v --rmi all
docker-compose up --build
docker exec -it constructiq-backend python create_user.py
```

---

## Running Without Docker

If you prefer running natively:

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:pass@localhost:5432/construct_iq"
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Make sure you have a PostgreSQL instance running locally.
