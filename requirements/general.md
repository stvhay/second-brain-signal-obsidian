# General Requirements

## Description

This document defines system-level functional requirements and cross-cutting requirements that apply to all components of the second-brain system.

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

## System Functional Requirements

### Capture

> See: [Capture](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=550), [Key Principles](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=1029)

1. [SYS-001] The system shall accept user input from multiple channels (e.g., messaging apps, voice, mobile apps, desktop).
2. [SYS-002] The system shall accept multiple input modalities including text, voice, images, and video.
3. [SYS-003] The system shall not require the user to classify or organize content at capture time.
4. [SYS-004] The system shall accept raw, unstructured input without requiring specific formatting.
5. [SYS-005] The system shall support single-action capture from any open channel.

### Organization

> See: [Sorter](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=603), [AI Classification](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=654), [Form/Schema](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=661)

6. [SYS-006] The system shall automatically classify content into user-defined categories.
7. [SYS-007] The system shall automatically extract structured metadata from content, including but not limited to: dates, people, tags, and project references.
8. [SYS-008] The system shall automatically route content to appropriate locations based on classification and inferred patterns.
9. [SYS-009] The system shall assign a confidence score to each classification, extraction, and routing decision.
10. [SYS-010] The system shall act autonomously when confidence exceeds user-configured thresholds.
11. [SYS-011] The system shall use consistent schemas to enable automation and querying.

### Preservation

> See: [Filing Cabinet](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=718), [Receipt/Audit Trail](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=766)

12. [SYS-012] The system shall preserve the original captured content unchanged, regardless of transformations applied.
13. [SYS-013] The system shall log every decision with the reasoning that led to it.
14. [SYS-014] The system shall maintain a complete audit trail of what came in, what the system did with it, and the confidence level.
15. [SYS-015] The system shall enable users to trace any stored item back to its original capture and the decisions made about it.
16. [SYS-016] The system shall store content in a format that is human-readable and directly editable.

### Trust

> See: [Bouncer](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=809), [Fix Button](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=978), [Trivial Corrections](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=1025)

17. [SYS-017] The system shall not file content when confidence is below configured thresholds; it shall ask for clarification instead.
18. [SYS-018] The system shall prevent low-quality or uncertain outputs from polluting the user's knowledge base.
19. [SYS-019] The system shall support single-action correction of any decision.
20. [SYS-020] The system shall confirm what it did after each action, including confidence level.
21. [SYS-021] The system shall learn from user corrections to improve future decisions.
22. [SYS-022] The system shall explain its reasoning when asking for clarification.

### Communication

> See: [Tap on the Shoulder](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=865), [Weekly Review](https://www.youtube.com/watch?v=0TpON5T-Sw4&t=936)

23. [SYS-023] The system shall proactively deliver relevant information to the user without requiring the user to search.
24. [SYS-024] The system shall provide configurable periodic summaries (e.g., daily digest, weekly review).
25. [SYS-025] The system shall surface items needing user attention (low confidence, pending clarifications, stale items).
26. [SYS-026] The system shall deliver messages through user-preferred channels.
27. [SYS-027] The system shall support multi-turn conversations when resolving ambiguity.

### Access

28. [SYS-028] The system shall make stored content accessible from multiple devices.
29. [SYS-029] The system shall synchronize content to user-configured destinations.
30. [SYS-030] The system shall notify external systems when content changes.
31. [SYS-031] The system shall support user export of all stored content.

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
