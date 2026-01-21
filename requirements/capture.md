# Capture Requirements

## Description

The capture system receives user notes and sends them for processing. It also receives and displays processing output.

## Design Constraints

- The capture system is stateless for conversation context. It performs message-passing only.
- The processing system manages multi-turn conversation state and correlates replies.
- Each implementation defines its own transport mechanism.
- Upstream components handle user consent for location data.

## Functional Requirements

1. [CAP-001] The system shall record when the user created input as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) (preferred) or [RFC 2822](https://datatracker.ietf.org/doc/html/rfc2822#section-3.3) timestamp.
2. [CAP-002] The system shall assign a valid [type](capture-types.md) to each input.
3. [CAP-003] The system shall encode input into a supported format (see [capture-encoding.md](capture-encoding.md)).
4. [CAP-004] The system shall transmit encoded input to the [processing](process.md) system.
5. [CAP-005] The system shall display outbound messages from the [processing](process.md) system to the user (see Outbound Message Requirements). Responses may arrive via a different capture system.
6. [CAP-006] The system shall assign a unique identifier to each input message. Valid formats include [UUID](https://datatracker.ietf.org/doc/html/rfc9562.html) or cryptographic hash (SHA-1, SHA-256 per [FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final)).
7. [CAP-007] The system shall include its unique identifier (UUID or cryptographic hash) in each message.
8. [CAP-008] The system shall identify the encoding specification used (e.g., `messaging-001`, `changeset-001`).
9. [CAP-009] The system should include GPS location when available.
10. [CAP-010] The system may receive confirmation that the processing system handled a message. Confirmation handling is implementation-specific.

## Reliability Requirements

11. [CAP-011] The system shall persist outbound messages until the processing system confirms receipt.
12. [CAP-012] The system shall persist inbound messages until delivered to the user.
13. [CAP-013] The system shall never drop messages.
14. [CAP-014] The system shall log system failures (e.g., processing unavailability, attachment retrieval failures) and notify the user.

## Outbound Message Requirements

15. [CAP-015] The system shall receive outbound messages in these categories:
    - `fix` - request for user clarification on a specific item
    - `summary` - periodic digest of activity
    - `review` - items needing user attention
    - `prompt` - proactive reflection or reminder
16. [CAP-016] Each implementation shall declare which outbound message categories it supports.
17. [CAP-017] The system shall deliver supported outbound messages to the user.
18. [CAP-018] The system shall accept user responses to outbound messages and transmit them to the Processing system.
19. [CAP-019] If the system receives an outbound message category it does not support, it shall reject the message so Processing can fall back to an alternative Capture system.

## Capability Declaration

20. [CAP-020] The system shall declare its capabilities to the Processing system at registration or startup.
21. [CAP-021] Capability declaration shall include:
    - Supported outbound message categories
    - Supported input types (text, audio, image, video)
    - Maximum attachment size (if different from default)
22. [CAP-022] The system shall update its capability declaration if capabilities change during operation.

## Initialization Requirements

23. [CAP-023] The system should request the maximum attachment size limit from the processing system upon initialization.
24. [CAP-024] If the processing system does not provide a size limit, the system should use a default limit of 500 MB.
