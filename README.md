# 🛠️ The Production Readiness Exercise: `deploy-notifier-api`

You have inherited a "hackathon toy": a service that receives deployment events from CI/CD runners and forwards notifications to PagerDuty and an audit store.
It passed its initial demo, but it is an operational landmine.

Your mission: upgrade this service to meet the **5-Point Production Readiness Scorecard** in 50 minutes.

---

## 🚀 Getting Started

```bash
# Option A: local
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload        # Swagger UI at http://localhost:8000/docs
pytest                                # 2 tests fail. That's your starting point.

# Option B: container
docker compose up --build
```

Try it:

```bash
curl -X POST localhost:8000/api/v1/deployments \
  -H 'content-type: application/json' \
  -d '{"service":"auth-service","environment":"production","commit_sha":"a1b2c3d","author":"dev@company.com"}'
```

(Run it a few times against `production` and watch what happens.)

---

## 🎯 The 5-Point Scorecard

- [ ] **1. Strict API Contract**: Enforce payload validation with Pydantic schemas. Invalid payloads must return HTTP 422 with descriptive error messages.
- [ ] **2. ADR (Architectural Decision Record)**: Add `docs/adr/0002-async-notifications-vs-sync.md` explaining why synchronous webhook dispatching is a risk and how you mitigated it.
- [ ] **3. Feature Flag / Kill-Switch**: Wrap the flaky PagerDuty integration in an environment-driven kill-switch (`FEATURE_PAGERDUTY_DISPATCH=true/false`). If disabled or failing, degrade gracefully (return 202 Accepted).
- [ ] **4. Structured JSON Logging**: Replace all `print()` calls with structured JSON logs containing timestamp, level, message, and context fields (`service`, `environment`).
- [ ] **5. Correlation ID & Trace Propagation**: Middleware must extract incoming `x-trace-id` (or generate one if missing), attach it to the request state, include it in every log entry, and return it in the response header.

**Bonus (Versioning):** `APP_VERSION` is hardcoded. Propose how Conventional Commits (`feat!:`) + a semantic-release check would stop a breaking field change from shipping silently.

---

## ⏱️ Step-by-Step Sprints (50 mins)

### Sprint 1: Lock the Contract & Document the Why (15 min)
1. Replace `request.json()` with a strict Pydantic model (`DeploymentEventRequest`).
2. Require: `service` (str), `environment` (enum: `dev`, `staging`, `production`), `commit_sha` (hex, 7–40 chars), `author` (email).
3. Verify that `pytest tests/test_api.py::test_missing_required_fields_fails_silently` now passes.
4. Start your ADR in `docs/adr/` using the template in `0001-record-architecture-decisions.md`.

### Sprint 2: Shield Downstream & Add the Kill-Switch (15 min)
1. In `app/downstream.py`, PagerDuty hangs for 3s and randomly throws 504s for `production` deploys.
2. Add an environment-driven flag: `FEATURE_PAGERDUTY_DISPATCH` (default `false`).
3. If the flag is off **or** the call fails, skip/swallow it, write the audit record, log a bypass, and return `202 Accepted` with `{"status": "queued_locally"}` instead of hanging or 500-ing.
4. Finish your ADR: why sync, what you rejected (retry loops? a queue?), and the consequences.

### Sprint 3: Turn on the Lights (20 min)
1. Add a FastAPI middleware that reads `x-trace-id`; if missing, generate a UUID.
2. Return `x-trace-id` in the response headers.
3. Replace every `print()` with a structured JSON logger (`structlog` or a stdlib `logging` JSON formatter).
4. Ensure every log line emitted during a request automatically includes `trace_id`.
5. Verify `pytest tests/test_api.py::test_trace_id_propagated_in_response` passes.

**Done when:** `pytest` is fully green, `FEATURE_PAGERDUTY_DISPATCH=false` returns 202 for production deploys, and a single request produces a clean, correlated JSON log stream.
