# Processing Requirements

## Description

The Processing system receives encoded messages from Capture, applies AI-powered classification and routing, and writes content to Storage. It operates autonomously for high-confidence decisions and solicits user input via Fix requests when uncertain. It also triggers scheduled prompts for summaries, reviews, and reflections.

## Design Constraints

- Processing is the sole writer to Storage.
- Processing reads user-defined schema and preferences from Storage.
- Processing infers routing patterns by examining existing vault content.
- Classification categories and confidence thresholds are user-configurable, not hardcoded.
- The processing log is the source of truth for conversation state and learning.
- Outbound messages (Fix, summaries, prompts) route through Capture systems based on user preferences.
- Learning mechanisms are implementation-defined; robust logging supports them.

## Relationship to Other Systems

| System | Processing Role |
|--------|-----------------|
| Capture | Receives inbound messages; sends outbound messages (Fix, prompts) |
| Storage | Reads schema/preferences/content; writes processed notes and log |
| Publish | Monitors publish status; notifies user when distribution is blocked |

## Core Operations

1. [PROC-001] The system shall classify each inbound message against user-defined categories from the Storage schema.
2. [PROC-002] The system shall extract structured metadata from message content, including but not limited to: dates, people mentioned, tags, and project references.
3. [PROC-003] The system shall route each message to a destination in the vault by inferring patterns from existing vault content.
4. [PROC-004] The system shall transform raw captured content into properly formatted markdown with frontmatter conforming to the Storage schema.
5. [PROC-005] The system shall assign a confidence score (0.0 to 1.0) for each operation: classification, extraction, and routing.
6. [PROC-006] The system shall include brief reasoning with each decision explaining the basis for the classification, extraction, and routing choices.
7. [PROC-007] When all confidence scores exceed their configured thresholds, the system shall write the transformed content to Storage without user intervention.
8. [PROC-008] When any confidence score falls below its configured threshold, the system shall initiate a Fix request (see Fix Mechanism).
9. [PROC-009] The system shall preserve the original message content and metadata unchanged in the processing log, regardless of transformation applied.

## Fix Mechanism

10. [PROC-010] The system shall initiate a Fix request when any operation's confidence score falls below its configured threshold.
11. [PROC-011] Fix requests shall be sent via the originating Capture system using the `captureContext` field to enable capture-system-specific handling.
12. [PROC-012] Fix requests shall be self-contained with sufficient context for single-message resolution:
    - The original captured content
    - The system's interpretation (classification, extracted data, proposed routing)
    - The specific uncertainty (which operation, confidence level, alternatives considered)
    - Clear options when applicable
13. [PROC-013] The system shall support multi-turn Fix conversations, allowing users to:
    - Provide a direct answer
    - Ask for more context ("why do you think this is a task?")
    - Offer corrections to any aspect of the interpretation
14. [PROC-014] The system shall reconstruct conversation state from the processing log; no separate state storage is required.
15. [PROC-015] Upon receiving a Fix response, the system shall re-evaluate confidence and either:
    - Proceed with filing if confidence thresholds are now met
    - Send a follow-up Fix request if ambiguity remains
16. [PROC-016] User corrections received via Fix shall be logged in detail for later analysis.

## Scheduling

17. [PROC-017] The system shall support user-configurable scheduled triggers for time-based prompts.
18. [PROC-018] Scheduled triggers shall support the following prompt types:
    - **Summary** - digest of captured items over a period
    - **Review** - items needing attention (low confidence, unresolved Fix requests, stale items)
    - **Prompt** - proactive reflection or reminders based on vault content (e.g., project staleness)
19. [PROC-019] The system shall allow users to configure schedule frequency (e.g., daily, weekly) and timing for each prompt type.
20. [PROC-020] Scheduled prompts shall be:
    - Logged in the vault via Storage
    - Sent to the user via Capture system based on outbound message preferences
21. [PROC-021] The system shall read schedule configuration from the Storage schema.
22. [PROC-022] The system shall evaluate vault state at trigger time to generate contextually relevant prompts (not static templates).
23. [PROC-023] Scheduled prompts that solicit user response shall be tracked as conversations and follow the same log-based state reconstruction as Fix conversations.

## Logging

24. [PROC-024] The system shall log every processed message with the following information:
    - Original message ID and content reference
    - Timestamp for each processing stage
    - Classification decision with confidence score and reasoning
    - Extraction results with confidence scores and reasoning
    - Routing decision with confidence score and reasoning
    - Transformation applied
    - Schema version active at processing time
    - Whether Fix was triggered and for which operation(s)
25. [PROC-025] The system shall log all Fix conversations:
    - Outbound Fix request content
    - User response content and timestamp
    - Resolution outcome (filed, follow-up sent, abandoned)
26. [PROC-026] The system shall log all scheduled prompts:
    - Trigger type and configuration
    - Generated prompt content
    - User response (if any)
27. [PROC-027] The system shall enable detection of manual corrections by correlating Storage's commit log against processing decisions. Manual corrections are surfaced via Capture systems (e.g., a file-watching Capture implementation detects vault changes and sends them as `changeset-001` messages).
28. [PROC-028] The processing log shall support querying by:
    - Message ID (full history of a single item)
    - Time range
    - Confidence score ranges
    - Fix status (triggered, resolved, pending)
29. [PROC-029] The processing log shall be the sole source of truth for conversation state and retrospective analysis.

## Configuration & Schema

30. [PROC-030] The system shall read classification categories from the Storage schema.
31. [PROC-031] The system shall read confidence thresholds from the Storage schema as a matrix of operation × category (e.g., routing threshold for "task" may differ from routing threshold for "note").
32. [PROC-032] The system shall provide default confidence thresholds when user-defined thresholds are not specified.
33. [PROC-033] The system shall support threshold adjustment via natural language interaction with the LLM (e.g., "be more careful when routing tasks").
34. [PROC-034] Threshold changes shall be persisted to the Storage schema and logged.
35. [PROC-035] The system shall read outbound message routing preferences from the Storage schema, specifying which Capture system(s) handle each message type (fix, summary, review, prompt) with priority ordering.
36. [PROC-036] The system shall read schedule configuration from the Storage schema, including frequency, timing, and enabled prompt types.
37. [PROC-037] The system shall validate configuration at startup and emit clear error messages for invalid or missing required configuration.
38. [PROC-038] The system shall support configuration changes without restart; changes to schema shall be detected and applied.

## Outbound Messages

39. [PROC-039] The system shall support the following outbound message categories:
    - `fix` - request clarification on a specific item
    - `summary` - periodic digest of activity
    - `review` - items needing user attention
    - `prompt` - proactive reflection or reminder
40. [PROC-040] The system shall route outbound messages to Capture systems based on:
    - User-defined preferences per message category (from Storage schema)
    - Capture system declared capabilities (which message types it supports)
    - Priority ordering when multiple Capture systems are configured for a category
41. [PROC-041] The system shall fall back to the next preferred Capture system if the primary is unavailable or does not support the message category.
42. [PROC-042] The system shall log outbound message routing decisions, including which Capture system was selected and why.
43. [PROC-043] Outbound messages shall be self-contained and clear. Processing reconstructs conversation context from its logs rather than requiring explicit threading in messages.
44. [PROC-044] The system shall track pending outbound messages awaiting response and surface them in scheduled review prompts.

## Storage Interaction

45. [PROC-045] The system shall read from Storage to:
    - Obtain user-defined schema (categories, thresholds, preferences, schedules)
    - Examine existing vault content for routing pattern inference
    - Detect manual corrections by analyzing Storage commit history
46. [PROC-046] The system shall write to Storage:
    - Transformed notes with frontmatter conforming to the schema
    - Processing log entries
    - Scheduled prompt records
    - Configuration updates (e.g., threshold adjustments)
47. [PROC-047] All writes to Storage shall conform to the user-defined schema; the system shall not write content that would fail schema validation.
48. [PROC-048] The system shall respect Storage's role as owner of the vault; Processing shall not bypass Storage's validation or write directly to the filesystem except as an implementation optimization when co-located.
49. [PROC-049] When routing inference examines vault content, the system shall use the current schema version and log which content influenced the routing decision.
50. [PROC-050] The system shall handle Storage unavailability gracefully by queuing messages for retry and notifying the user via available Capture systems.

## Error Handling & Reliability

51. [PROC-051] The system shall default to safe behavior when uncertain: log the item and initiate a Fix request rather than filing incorrectly.
52. [PROC-052] The system shall quarantine messages that fail processing after retry attempts, logging the failure reason for manual review.
53. [PROC-053] The system shall continue processing other messages when one message fails; partial failures shall not halt the system.
54. [PROC-054] Message processing shall be idempotent; reprocessing a message shall produce consistent results.
55. [PROC-055] The system shall persist inbound messages until successfully processed or quarantined.
56. [PROC-056] The system shall gracefully drain pending work before shutdown.
57. [PROC-057] The system should process messages within a configurable time limit; messages exceeding the limit shall be logged and may trigger a Fix request indicating processing complexity.

## Publish Status Monitoring

58. [PROC-058] The system shall monitor Publish status indicators exposed per PUB-008.
59. [PROC-059] When Publish indicates distribution is blocked or delayed, the system shall notify the user via the configured Capture system for `review` messages.
60. [PROC-060] Publish status notifications shall include:
    - Which channel is affected
    - Reason for the block (if available from the status indicator)
    - Duration of the block
    - Suggested user action (if applicable)

## Cross-Cutting Requirements

See [general.md](general.md) for logging format, observability, security, and versioning requirements that apply to all components.
