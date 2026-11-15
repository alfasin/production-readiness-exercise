import random
import time

# Stand-in for the real PagerDuty client. Do not modify: treat this as a
# third-party system you don't control.


def call_pagerduty_webhook(payload: dict) -> str:
    if payload.get("environment") == "production":
        time.sleep(3)
        if random.random() < 0.4:
            raise ConnectionError("504 Gateway Timeout: PagerDuty upstream unavailable")
    return "delivered"


def log_to_audit_store(payload: dict) -> None:
    pass
