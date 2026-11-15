# 🛠️ Production Readiness Exercise: `deploy-notifier-api`

## The Handover

The engineer who built this service left last Friday. It was a hackathon project that "just worked" in the demo, so it went live.

`deploy-notifier-api` receives deployment events from CI/CD runners and forwards them to PagerDuty and an audit store. As of this morning it's **yours**.

During last night's production release window, CI pipelines started hanging, on-call couldn't figure out which request caused what, and a downstream team swears they "sent the right payload."

You have **50 minutes** to make this service something you'd be willing to be paged for.

---

## 🚀 Getting Started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload        # Swagger UI at http://localhost:8000/docs
pytest
```

or `docker compose up --build`.

Poke at it:

```bash
curl -X POST localhost:8000/api/v1/deployments \
  -H 'content-type: application/json' \
  -d '{"service":"auth-service","environment":"production","commit_sha":"a1b2c3d","author":"dev@company.com"}'
```

Try different payloads and environments. Send it things a careless caller might send. Run it more than once.

> `app/downstream.py` simulates a third-party API you don't own. Don't fix the problem by editing it.

---

## 🎯 The 5-Point Scorecard

Each item describes *what done looks like*, not how to get there. The specifics in `code` are the contract your facilitator will check against.

- [ ] **1. Strict API Contract**: Malformed or incomplete deployment events are rejected at the boundary with `422` and an error a caller can act on. The contract is discoverable without reading the source.
- [ ] **2. Institutional Memory**: A new ADR in `docs/adr/` records one significant decision you made today: the context, the options you rejected, and the trade-offs you accepted. Use the template in `0001`.
- [ ] **3. Kill-Switch**: The PagerDuty integration can be turned off without a redeploy via `FEATURE_PAGERDUTY_DISPATCH`. Whether it's off or PagerDuty is misbehaving, callers still get a timely `202 Accepted` and the event is not silently lost.
- [ ] **4. Structured Logging**: Every log line is machine-parseable and carries enough context to answer "which service, which environment, what happened?"
- [ ] **5. Trace Propagation**: A caller-supplied `x-trace-id` (or a generated one, if absent) appears in the response headers and on every log line emitted while handling that request.

**Stretch: Versioning.** Look at how this service is versioned. What stops someone from shipping a breaking change to the payload without callers finding out first? Propose (or implement) a fix.

---

## ⏱️ Suggested Timebox

| Sprint | Time | Scorecard items |
|---|---|---|
| 1. Lock the contract & write down the why | 15 min | 1, 2 |
| 2. Shield the downstream | 15 min | 3 |
| 3. Turn on the lights | 20 min | 4, 5 |

**You're done when** `pytest` is green, the scorecard items hold up when your facilitator pokes at your running service, and you've added tests that prove items 3–5 too.
