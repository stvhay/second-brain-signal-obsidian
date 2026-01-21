# Capture Requirements

## Description

The capture system receives user notes and sends them for processing. It also receives and displays processing output.

## Design Constraints

- The capture system is stateless for conversation context. It performs message-passing only.
- The processing system manages multi-turn conversation state and correlates replies.
- The transport mechanism between Capture and Processing is implementation-specific.
- Upstream components handle user consent for location data.

## Functional Requirements

1. The system shall record the date and time the user created input as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) UTC timestamp string (e.g., `2026-01-19T21:21:56.000Z`).
2. The system shall assign a valid [type](capture-types.md) to input received.
3. The system shall encode input into a format defined in [capture-encoding](capture-encoding.md).
4. The system shall transmit encoded input to the [processing](process.md) system.
5. The system shall receive output from the [processing](process.md) system and display it to the user.
6. The system shall assign a [UUID](https://datatracker.ietf.org/doc/html/rfc9562.html) to each input message.
7. The system shall include its unique identifier (UUID) in each message.
8. The system shall identify the encoding specification used (e.g., `messaging-001`).
9. The system should include GPS location when available.
10. The system may receive confirmation that the processing system handled a message. Confirmation handling is implementation-specific.

## Reliability Requirements

11. The system shall persist outbound messages to disk until the processing system confirms receipt.
12. The system shall persist inbound messages to disk until it confirms delivery to the user.
13. The system shall not drop messages under any circumstances.

## Initialization Requirements

14. The system shall request the maximum attachment size limit from the processing system upon initialization.
15. If the processing system does not provide a size limit, the system shall use a default limit of 500 MB.
