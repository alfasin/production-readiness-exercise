from fastapi import FastAPI, Request

from app.downstream import call_pagerduty_webhook, log_to_audit_store

# ANTI-PATTERN: Hardcoded version, no semver / release automation
APP_VERSION = "0.1.0"

app = FastAPI(title="Deploy Notifier Service", version=APP_VERSION)

# ANTI-PATTERN: Raw prints, no request context or structured fields
print(f"Starting Deploy Notifier Service v{APP_VERSION}...")


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}


@app.post("/api/v1/deployments")
async def trigger_deployment_notification(request: Request):
    """
    ANTI-PATTERN 1 (Contract): Accepts raw unvalidated dict.
    ANTI-PATTERN 2 (Observability): print() statements instead of JSON logging.
    ANTI-PATTERN 3 (Tracing): Discards 'x-trace-id' / correlation headers.
    ANTI-PATTERN 4 (Feature Flags): Unguarded, synchronous downstream call.
    """
    payload = await request.json()

    # Trap: typos like team_id vs teamId pass silently until crashing downstream
    service_name = payload.get("service")
    environment = payload.get("environment")

    print(f"Received deployment event for {service_name} on {environment}")

    # ANTI-PATTERN: Blocking call to third-party webhook with no timeout guard or kill-switch
    print("Forwarding alert to PagerDuty...")
    pd_status = call_pagerduty_webhook(payload)
    print(f"PagerDuty responded with status: {pd_status}")

    # Audit log entry
    log_to_audit_store(payload)

    return {
        "status": "dispatched",
        "service": service_name,
        "environment": environment,
        "delivery_status": pd_status,
    }
