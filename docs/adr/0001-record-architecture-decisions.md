# [Short title of architectural decision]

* **Status**: [Proposed | Accepted | Deprecated | Superseded]
* **Date**: YYYY-MM-DD
* **Deciders**: [Names]

## Context and Problem Statement
What problem were we facing? (e.g., synchronous webhook dispatching in request handlers causes cascade failures when downstream APIs hang).

## Considered Options
* Option 1: Direct synchronous HTTP requests with retry loops.
* Option 2: Feature-flagged execution with timeout fallbacks.
* Option 3: Background tasks / Redis message queue.

## Decision Outcome
Chosen option: [Option X], because:
* [Justification 1]
* [Justification 2]

## Consequences
* **Positive**: [...]
* **Negative**: [...]
