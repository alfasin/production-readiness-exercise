import random
import time


def call_pagerduty_webhook(payload: dict) -> str:
    """Simulates an external webhook call with intermittent latency & 504s."""
    # Simulate a network hiccup when deploying to 'production'
    if payload.get("environment") == "production":
        # Simulate a 3-second network freeze (blocks the event loop!)
        time.sleep(3)
        if random.random() < 0.4:
            raise ConnectionError("504 Gateway Timeout: PagerDuty upstream unavailable")
    return "delivered"


def log_to_audit_store(payload: dict) -> None:
    # Simulates an unindexed database call
    pass
