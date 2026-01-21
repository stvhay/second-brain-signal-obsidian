# Capture - Signal Implementation

## Description

This implementation uses Signal "Note to Self" as the capture interface, with signal-cli REST API as the backend. Users send messages to themselves in Signal; the capture system receives these via the API, transforms them to canonical format, and forwards to processing.

## Components

| Component | Description |
|-----------|-------------|
| Signal app | User-facing interface (iOS/Android/Desktop) |
| signal-cli REST API | Receives messages, serves attachments |
| Capture service | Transforms Signal messages to canonical format |

## Architecture Note

The signal-cli REST API operates as a **linked device** on the user's Signal account. Users establish this link via QR code during setup, similar to Signal Desktop. As a linked device, signal-cli:

- Receives all messages sent to/from the account (including Note to Self)
- Can send messages on behalf of the account
- Does not require the primary phone to be online after initial linking

## Configuration

| Parameter | Description |
|-----------|-------------|
| `apiBase` | Base URL of signal-cli REST API |
| `number` | Registered phone number |
| `captureSystemId` | UUID v4 identifying this capture instance |
| `encodingId` | Encoding specification identifier (default: `messaging-001`) |
| `mqtt.broker` | MQTT broker URL |
| `mqtt.outboundTopic` | Topic for messages to Processing (e.g., `capture/outbound`) |
| `mqtt.inboundTopic` | Topic for messages from Processing (e.g., `capture/inbound`) |

## signal-cli REST API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/receive/{number}` | GET | Retrieve pending messages |
| `/v2/send` | POST | Send message to user |
| `/v1/attachments/{id}` | GET | Retrieve attachment by ID |
| `/v1/attachments` | GET | List all downloaded attachments |
| `/v1/about` | GET | API version and capabilities |
| `/v1/remote-delete/{number}` | DELETE | Delete a message |

### Receiving Messages

Messages are retrieved via `GET /v1/receive/{number}`. The response contains an array of message envelopes. Note to Self messages appear as `syncMessage.sentMessage` where destination equals source.

### Sending Messages

Responses to user are sent via `POST /v2/send`:

```json
{
  "number": "{configured_number}",
  "recipients": ["{configured_number}"],
  "message": "Response text"
}
```

For media attachments, include `base64_attachments` array.

### Attachments

Attachments are retrieved via `GET /v1/attachments/{id}` where `id` is the full attachment identifier including extension (e.g., `jDGRErTC-QFHpZUdKkkW.jpeg`).

### Deleting Messages

Messages are deleted via `DELETE /v1/remote-delete/{number}` with request body:

```json
{
  "recipient": "{configured_number}",
  "timestamp": 1737330116000
}
```

## Implementation

### 1. Timestamp Recording

The system extracts `envelope.timestamp` from the Signal message, which is a Unix timestamp in milliseconds. It converts this to ISO 8601 UTC format.

| Signal Field | Transformation |
|--------------|----------------|
| `envelope.timestamp` | Convert from Unix ms to ISO 8601 UTC (e.g., `2026-01-19T21:21:56.000Z`) |

### 2. Type Assignment

Type is derived from message content:

| Condition | Assigned Type |
|-----------|---------------|
| `syncMessage.sentMessage.message` is non-null | `text` |
| Attachment `contentType` starts with `audio/` | `audio` |
| Attachment `contentType` starts with `image/` | `image` |
| Attachment `contentType` starts with `video/` | `video` |

A message with text and attachments produces multiple content items.

### 3. Encoding

The system transforms Signal's message format to the `messaging-001` encoding:

| Signal Field | Encoded Field |
|--------------|---------------|
| (generated) | `id` |
| (constant) | `encodingId` → `"messaging-001"` |
| (configured) | `captureSystemId` |
| `envelope.timestamp` | `timestamp` (ISO 8601 UTC) |
| (not available) | `location` → `null` |
| `syncMessage.sentMessage.message` | `content[].type: "text", data: <message>` |
| `syncMessage.sentMessage.attachments[]` | `content[].type: <derived>, data: <media object>` |
| `envelope.timestamp` | `captureContext.signalTimestamp` |

**Attachment to Media Object Mapping:**

| Signal Attachment Field | Media Object Field |
|------------------------|-------------------|
| `id` | `id` |
| `filename` | `filename` |
| `contentType` | `contentType` |
| `size` | `size` |
| (constructed) | `retrievalUrl` → `{apiBase}/v1/attachments/{id}` |

### 4. Transmission to Processing

The capture service publishes encoded messages to the processing system via MQTT.

| Field | Value |
|-------|-------|
| Broker | Configured MQTT broker |
| Topic | Configured outbound topic (e.g., `capture/outbound`) |
| Payload | `messaging-001` encoded message (JSON) |
| QoS | 1 (at least once delivery) |

### 5. Receiving from Processing

The capture service subscribes to the inbound MQTT topic and sends received messages to the user via Signal:

| Processing Output | Signal Action |
|-------------------|---------------|
| Text response | Send message via `POST /v2/send` |
| Media attachment | Send with `base64_attachments` field |

Messages are sent to the user's own number (Note to Self).

### 6. UUID Assignment

Signal identifies messages by timestamp. The capture system generates a UUID v4 for the message `id` field.

| Field | Source |
|-------|--------|
| `id` | Generated UUID v4 |
| `captureSystemId` | Configured UUID v4 for this deployment |

### 7. Processing Confirmation (Optional)

If confirmation handling is enabled, the capture service deletes the original message from Signal upon receiving confirmation using `DELETE /v1/remote-delete/{number}`.

The processing system returns the message with `captureContext` intact. The capture service extracts `captureContext.signalTimestamp` to identify the message for deletion.

| Confirmation Field | Description |
|--------------------|-------------|
| `id` | UUID of the processed message |
| `captureContext.signalTimestamp` | Original Signal timestamp for deletion |

## Reliability

### Persistent Message Queue

The capture service maintains a persistent disk queue for both inbound and outbound messages:

| Queue | Purpose |
|-------|---------|
| Outbound queue | Messages awaiting transmission to processing system |
| Inbound queue | Responses from processing awaiting delivery to Signal |

The system removes messages from the queue only after confirming transmission. The system never drops messages.

### Failure Handling

| Failure Scenario | Behavior |
|------------------|----------|
| Processing system unavailable | Message remains in outbound queue; retry with backoff |
| Signal send fails | Response remains in inbound queue; retry with backoff |
| Service restart | Queues are restored from disk; processing resumes |

## Initialization

Upon startup, the capture service:

1. Requests the maximum attachment size limit from the processing system
2. If the processing system does not provide a limit, uses the default of 500 MB
3. Rejects attachments exceeding this limit with an error message to the user
