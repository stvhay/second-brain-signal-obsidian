# Capture Requirements

## Description

The capture system receives user notes and sends them for processing. It also receives and displays processing output.

## Design Constraints

- The capture system is stateless for conversation context. It performs message-passing only.
- The processing system manages multi-turn conversation state and correlates replies.
- Each implementation defines its own transport mechanism.
- Upstream components handle user consent for location data.

## Functional Requirements

1. The system shall record when the user created input as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) (preferred) or [RFC 2822](https://datatracker.ietf.org/doc/html/rfc2822#section-3.3) timestamp.
2. The system shall assign a valid [type](capture-types.md) to each input.
3. The system shall encode input into a supported format (see [capture-encoding.md](capture-encoding.md)).
4. The system shall transmit encoded input to the [processing](process.md) system.
5. The system shall display output from the [processing](process.md) system to the user. Responses may arrive via a different capture system.
6. The system shall assign a unique identifier to each input message. Valid formats include [UUID](https://datatracker.ietf.org/doc/html/rfc9562.html) or cryptographic hash (SHA-1, SHA-256 per [FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final)).
7. The system shall include its unique identifier (UUID) in each message.
8. The system shall identify the encoding specification used (e.g., `messaging-001`, `changeset-001`).
9. The system should include GPS location when available.
10. The system may receive confirmation that the processing system handled a message. Confirmation handling is implementation-specific.

## Reliability Requirements

11. The system shall persist outbound messages until the processing system confirms receipt.
12. The system shall persist inbound messages until delivered to the user.
13. The system shall never drop messages.

## Initialization Requirements

14. The system should request the maximum attachment size limit from the processing system upon initialization.
15. If the processing system does not provide a size limit, the system should use a default limit of 500 MB.
