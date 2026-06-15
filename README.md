# 🛒 backend_endpoint

High-throughput **`/purchase`** endpoint built to survive flash-sale traffic:
hundreds of concurrent purchase requests for a **limited-stock product**,
without overselling and without melting the database. 🔥

---

## 🚀 What it does

1. 📥 Client sends `POST /purchase` with `user_id`, `product_id`,
   `purchased_count`.
2. ⚡ Stock is decremented **atomically in Redis** via a Lua script —
   this is the hot path, no database round-trip on the request.
3. 📨 If the decrement succeeds, a **Celery task** is queued (via
   RabbitMQ) to asynchronously sync the new stock value back to
   **Postgres**.
4. ✅ Response is returned to the client immediately — `success`,
   `not enough stock`, or `product not found`.

```
Client ──▶ FastAPI ──▶ Redis (atomic DECRBY via Lua)
                │
                └──▶ RabbitMQ ──▶ Celery worker ──▶ Postgres
```

---

## 🧱 Tech stack

| Layer | Tech |
|---|---|
| 🌐 Web framework | FastAPI + Granian (ASGI) |
| ⚡ Cache / hot path | Redis (Lua script for atomic stock decrement) |
| 🐘 Database | PostgreSQL + SQLAlchemy (async, asyncpg) |
| 📨 Task queue | Celery + RabbitMQ |
| 🔄 Migrations | Alembic |
| 📦 Dependency management | uv |
| 🐳 Containerization | Docker Compose |
| 🐝 Load testing | Locust |

---

## 📂 Project structure

```
app/
├── cache/          # Redis client + atomic Lua scripts
├── db/             # SQLAlchemy models & repository layer
├── exceptions/     # Custom HTTP exceptions
├── worker/         # Celery app + background sync tasks
├── router.py       # /purchase endpoint
├── schemas.py      # Pydantic request/response models
├── session.py      # Async SQLAlchemy engine & session factory
└── settings.py     # Environment-based settings

migrations/          # Alembic migrations
tests/               # Test suite
seed.py              # Seed initial product stock
```

---

## ⚙️ Setup

### 1. Configure environment

Create a `.env` file:

```env
PG_DNS=postgresql+asyncpg://user:password@postgres:5432/shop
REDIS_DNS=redis://redis:6379/0
AMQP_DNS=amqp://guest:guest@rabbitmq:5672//
```

### 2. Run with Docker Compose 🐳

```bash
docker compose up --build
```

This spins up:
- 🌐 `api` — FastAPI app (Granian, 4 workers) on `:8000`
- 🐘 `postgres` — database on `:5432`
- ⚡ `redis` — cache on `:6379`
- 🐇 `rabbitmq` — broker + management UI on `:5672` / `:15672`
- 👷 `worker` — Celery worker syncing stock back to Postgres

Migrations run automatically on startup via `entrypoint.sh`.

### 3. Seed product stock 🌱

```bash
uv run python seed.py
```

---

## 📡 API

### `POST /purchase`

**Request**
```json
{
  "user_id": 1,
  "product_id": 1,
  "purchased_count": 2
}
```

**Responses**
| Status | Meaning |
|---|---|
| ✅ `200` | Purchase successful |
| ❌ `404` | Product not found |
| ❌ `409` | Not enough stock |

---

## 🧪 Load testing

```bash
uv run locust -f tests/locustfile.py
```

Verified to handle **~650 RPS** with **0 failures** and p99 latency under
250ms. 🚀

**Summary** (191k requests, 0 failures):

![Locust stats](tests/content/stats.png)

**RPS / response times / concurrent users over time:**

![Locust charts](tests/content/total_requests.png)

---
