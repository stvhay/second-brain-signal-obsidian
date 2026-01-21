# General Requirements

## Description

This document defines cross-cutting requirements that apply to all components of the second-brain system.

## Scope

The system is designed for single-user operation. Multi-user and collaboration are out of scope.

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

1. [GEN-001] The system shall provide a User Guide explaining how to capture notes, expected system behavior, and troubleshooting steps.
2. [GEN-002] The system shall provide an Operations Guide covering deployment, configuration, monitoring, and maintenance procedures.
3. [GEN-003] The system shall provide API Documentation for each component interface.
4. [GEN-004] The system shall provide an Architecture Overview describing system context, component relationships, and data flows.
5. [GEN-005] The system shall maintain a Changelog with version history; breaking changes shall be clearly marked.

## Logging & Observability Requirements

6. [GEN-006] All components shall emit structured logs in JSON format.
7. [GEN-007] All components shall include a correlation ID (message UUID) in log entries to enable end-to-end tracing.
8. [GEN-008] All components shall support configurable log levels: DEBUG, INFO, WARN, ERROR.
9. [GEN-009] Each service shall expose a health check endpoint indicating readiness status.
10. [GEN-010] Each service should expose operational metrics including queue depth, processing latency, and error rates.

## Configuration Requirements

11. [GEN-011] All components shall support configuration via environment variables or configuration files.
12. [GEN-012] Sensitive configuration values (API keys, tokens, credentials) shall be stored separately from general configuration.
13. [GEN-013] All components shall validate configuration at startup and emit clear error messages for invalid configuration.
14. [GEN-014] Optional configuration parameters shall have sensible defaults.

## Security Requirements

15. [GEN-015] All network communication between components shall use TLS encryption.
16. [GEN-016] Components shall authenticate to each other before exchanging messages.
17. [GEN-017] The system shall encrypt sensitive data at rest (queues, attachments, credentials).
18. [GEN-018] The system shall log security-relevant events for auditing.

## Error Handling Requirements

19. [GEN-019] Partial failures in one component shall not cause total system failure.
20. [GEN-020] The system shall inform users of errors in plain language.
21. [GEN-021] The system shall retry transient failures with exponential backoff and notify users of permanent failures.
22. [GEN-022] The system shall quarantine unprocessable messages for manual review (dead letter queue).

## Data Management Requirements

23. [GEN-023] The system shall support configurable retention periods for logs, queues, and attachments.
24. [GEN-024] The system shall document backup and restore procedures.
25. [GEN-025] The system shall let users export their data.
26. [GEN-026] The system shall not collect telemetry or share data without explicit user consent.

## Versioning Requirements

27. [GEN-027] All components shall follow semantic versioning.
28. [GEN-028] Breaking API changes shall require a new API version.
29. [GEN-029] New encoding specifications shall receive new identifiers (e.g., `messaging-002`).
30. [GEN-030] The system shall document a compatibility matrix showing which component versions work together.

## Operational Requirements

31. [GEN-031] Components shall drain queues gracefully before stopping (graceful shutdown).
32. [GEN-032] Components shall verify dependencies are available at startup before accepting work.
33. [GEN-033] Components shall support configurable resource limits (memory, disk, connections).
34. [GEN-034] Message processing shall be idempotent; reprocessing a message shall produce consistent results.
