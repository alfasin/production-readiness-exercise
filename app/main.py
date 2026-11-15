from fastapi import FastAPI, Request

from app.downstream import call_pagerduty_webhook, log_to_audit_store

APP_VERSION = "0.1.0"

app = FastAPI(title="Deploy Notifier Service", version=APP_VERSION)

print(f"Starting Deploy Notifier Service v{APP_VERSION}...")


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}


@app.post("/api/v1/deployments")
async def trigger_deployment_notification(request: Request):
    payload = await request.json()

    service_name = payload.get("service")
    environment = payload.get("environment")

    print(f"Received deployment event for {service_name} on {environment}")

    print("Forwarding alert to PagerDuty...")
    pd_status = call_pagerduty_webhook(payload)
    print(f"PagerDuty responded with status: {pd_status}")

    log_to_audit_store(payload)

    return {
        "status": "dispatched",
        "service": service_name,
        "environment": environment,
        "delivery_status": pd_status,
    }
