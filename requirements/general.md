# General Requirements

## Description

This document defines cross-cutting requirements that apply to all components of the second-brain system.

## System Architecture

The second-brain comprises four systems:

| System | Purpose |
|--------|---------|
| [Capture](capture.md) | Receive user input, encode it, transmit to Processing, display responses |
| Processing | Classify notes, generate metadata, route by confidence |
| Storage | Persist notes in Obsidian, detect changes via git hooks |
| Publish | Notify external systems via MQTT, sync to iCloud |

See [architecture diagrams](../diagrams/) for data flow details.

## Documentation Requirements

1. The system shall provide a User Guide explaining how to capture notes, expected system behavior, and troubleshooting steps.
2. The system shall provide an Operations Guide covering deployment, configuration, monitoring, and maintenance procedures.
3. The system shall provide API Documentation for each component interface.
4. The system shall provide an Architecture Overview describing system context, component relationships, and data flows.
5. The system shall maintain a Changelog with version history; breaking changes shall be clearly marked.

## Logging & Observability Requirements

6. All components shall emit structured logs in JSON format.
7. All components shall include a correlation ID (message UUID) in log entries to enable end-to-end tracing.
8. All components shall support configurable log levels: DEBUG, INFO, WARN, ERROR.
9. Each service shall expose a health check endpoint indicating readiness status.
10. Each service should expose operational metrics including queue depth, processing latency, and error rates.

## Configuration Requirements

11. All components shall support configuration via environment variables or configuration files.
12. Sensitive configuration values (API keys, tokens, credentials) shall be stored separately from general configuration.
13. All components shall validate configuration at startup and emit clear error messages for invalid configuration.
14. Optional configuration parameters shall have sensible defaults.

## Security Requirements

15. All network communication between components shall use TLS encryption.
16. Components shall authenticate to each other before exchanging messages.
17. The system shall encrypt sensitive data at rest (queues, attachments, credentials).
18. The system shall log security-relevant events for auditing.

## Error Handling Requirements

19. Partial failures in one component shall not cause total system failure.
20. The system shall inform users of errors in plain language.
21. The system shall retry transient failures with exponential backoff and notify users of permanent failures.
22. The system shall quarantine unprocessable messages for manual review (dead letter queue).

## Data Management Requirements

23. The system shall support configurable retention periods for logs, queues, and attachments.
24. The system shall document backup and restore procedures.
25. The system shall let users export their data.
26. The system shall not collect telemetry or share data without explicit user consent.

## Versioning Requirements

27. All components shall follow semantic versioning.
28. Breaking API changes shall require a new API version.
29. New encoding specifications shall receive new identifiers (e.g., `messaging-002`).
30. The system shall document a compatibility matrix showing which component versions work together.

## Operational Requirements

31. Components shall drain queues gracefully before stopping (graceful shutdown).
32. Components shall verify dependencies are available at startup before accepting work.
33. Components shall support configurable resource limits (memory, disk, connections).
34. Message processing shall be idempotent; reprocessing a message shall produce consistent results.
