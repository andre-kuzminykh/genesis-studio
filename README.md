# Genesis Studio

PRD-first platform for bot/backend generation and GitHub delivery.

## Architecture

- **Backend**: FastAPI service (`backend/`) — data, business logic, integrations
- **Bot**: aiogram 3 Telegram bot (`bot/`) — UI only, all data via backend API
- **Database**: PostgreSQL with SQLAlchemy async ORM

## Quick Start

```bash
# 1. Start PostgreSQL
docker compose -f docker/docker-compose.yml up db -d

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Run migrations
alembic upgrade head

# 4. Start backend
./scripts/run_backend.sh

# 5. Start bot (in another terminal)
TELEGRAM_BOT_TOKEN=your-token ./scripts/run_bot.sh
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/products` | Create product from idea |
| POST | `/api/v1/products/{id}/discovery` | Submit discovery answer |
| POST | `/api/v1/products/{id}/features` | Generate feature map |
| POST | `/api/v1/products/{id}/features/approve` | Approve feature map |
| POST | `/api/v1/features/{id}/prd/draft` | Generate PRD draft |
| POST | `/api/v1/features/{id}/stories/approve` | Approve user stories |
| POST | `/api/v1/features/{id}/ux/generate` | Generate UX preview |
| POST | `/api/v1/features/{id}/use-cases/generate` | Generate use cases |
| POST | `/api/v1/features/{id}/use-cases/approve` | Approve use cases |
| POST | `/api/v1/features/{id}/requirements/generate` | Derive requirements |
| POST | `/api/v1/features/{id}/tests/generate` | Generate tests |
| POST | `/api/v1/features/{id}/tests/approve` | Approve tests |
| POST | `/api/v1/features/{id}/code/generate` | Generate code |
| POST | `/api/v1/features/{id}/github/push` | Push to GitHub |
| POST | `/api/v1/features/{id}/deploy/local` | Deploy locally |
| POST | `/api/v1/features/{id}/change-request` | Create change request |
| GET | `/api/v1/features/{id}/traceability` | Get traceability graph |
| POST | `/api/v1/github/connect/{product_id}` | Connect GitHub repo |

## Testing

```bash
./scripts/run_tests.sh
```

## Codegen Policy

All code generation follows the mandatory architectural policy:
- Bot = UI only (no DB, no ORM, no heavy logic)
- Backend = data + business logic
- Each project has `prd.json` as source of truth
- Order: PRD → gap analysis → tests → backend code → bot code
- Traceability required on all modules
