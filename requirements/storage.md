# Storage Requirements

## Description

The Storage system persists content and maintains the canonical state of the vault. It validates writes against a user-defined schema, maintains change history, and notifies Publish when content changes.

## Design Constraints

- Process is the sole writer to Storage.
- The schema is user-defined configuration, not prescribed by requirements.
- The message format between Storage and Publish is implementation-defined.

## Functional Requirements

1. [STOR-001] The system shall persist content to the file system.
2. [STOR-002] The system shall implement a user-defined schema.
3. [STOR-003] The system shall validate all writes against the schema.
4. [STOR-004] The system shall reject content that fails schema validation.
5. [STOR-005] The system shall accept schema updates from the Processing system.
6. [STOR-006] The system shall provide read access to the Processing system.
7. [STOR-007] The system shall provide write access to the Processing system, subject to schema validation.
8. [STOR-008] The system shall maintain change history.
9. [STOR-009] The system shall immediately notify Publish when content is accepted.
10. [STOR-010] The system shall support both text and binary attachments.

## Cross-Cutting Requirements

See [general.md](general.md) for logging, configuration, security, and error handling requirements that apply to all components.
