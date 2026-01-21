# Capture Encoding Standards

This document defines message encoding for bidirectional communication between Capture and Processing systems.

- **Inbound messages**: Capture → Processing (user input)
- **Outbound messages**: Processing → Capture (system responses)

Both directions use the same encoding specifications. Messages are self-contained; Processing reconstructs conversation state from its logs rather than requiring explicit threading.

---

## Encoding: `messaging-001`

The `messaging-001` encoding specification for messages between Capture and Processing.

### Inbound Example (Capture → Processing)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "encodingId": "messaging-001",
  "captureSystemId": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "timestamp": "2026-01-19T21:21:56.000Z",
  "location": null,
  "content": [
    { "type": "text", "data": "Check out this sunset" },
    {
      "type": "image",
      "data": {
        "id": "jDGRErTC-QFHpZUdKkkW.jpeg",
        "filename": "signal-2026-01-19-212156.jpeg",
        "contentType": "image/jpeg",
        "size": 141880,
        "retrievalUrl": "https://example.com/v1/attachments/jDGRErTC-QFHpZUdKkkW.jpeg"
      }
    }
  ],
  "captureContext": {}
}
```

### Outbound Example (Processing → Capture)

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "encodingId": "messaging-001",
  "timestamp": "2026-01-19T21:25:00.000Z",
  "content": [
    { "type": "text", "data": "I received 'Check out this sunset' with a photo. Should I file this as a journal entry, or is there a task here I should track?" }
  ],
  "captureContext": {}
}
```

## Top-Level Fields

| Field | Type | Direction | Required | Description |
|-------|------|-----------|----------|-------------|
| `id` | UUID/hash | Both | Yes | Unique message identifier |
| `encodingId` | string | Both | Yes | Encoding specification identifier (`messaging-001`) |
| `captureSystemId` | UUID | Inbound | Yes | Identifies the capture system instance |
| `timestamp` | string | Both | Yes | ISO 8601 UTC timestamp |
| `location` | object | Inbound | No | GPS coordinates if available |
| `content` | array | Both | Yes | One or more content items |
| `captureContext` | object | Both | No | Opaque object for capture system use. Processing includes this unchanged in responses to enable capture-system-specific handling. |

## Content Item Types

| Type | Data |
|------|------|
| `text` | `"string"` |
| `audio` | Media object |
| `image` | Media object |
| `video` | Media object |

## Media Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for this attachment |
| `filename` | string | Original filename |
| `contentType` | string | MIME type |
| `size` | integer | File size in bytes |
| `retrievalUrl` | string | Full URL to retrieve the attachment |

## Location Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `lat` | float | Latitude in decimal degrees |
| `lon` | float | Longitude in decimal degrees |
| `accuracy` | integer | Accuracy in meters |

---

## Encoding: `changeset-001`

A `changeset-001` message is a git patch. The commit itself serves as the canonical message format.

### Structure

```
From <sha> <date>
From: <capture-system-name> <email>
Date: <rfc-2822-timestamp>
Subject: [PATCH] encodingId: changeset-001

captureSystemId: <uuid>

---
<diffstat>

<diff content>
```

### Example

```
From a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0 Mon Jan 20 00:00:00 2026
From: capture-icloud <capture@second-brain.local>
Date: Mon, 20 Jan 2026 15:30:00 +0000
Subject: [PATCH] encodingId: changeset-001

captureSystemId: 6ba7b810-9dad-11d1-80b4-00c04fd430c8

---
 notes/project.md         | 3 ++-
 attachments/photo.jpg    | Bin 0 -> 141880 bytes
 2 files changed, 2 insertions(+), 1 deletion(-)

diff --git a/notes/project.md b/notes/project.md
index 1234567..abcdef0 100644
--- a/notes/project.md
+++ b/notes/project.md
@@ -10,6 +10,8 @@ Some existing content
+New content added by user
```

### Required Fields

| Field | Location | Description |
|-------|----------|-------------|
| Message ID | SHA in `From` line | Unique identifier (SHA-1 or SHA-256 per [FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final)) |
| Timestamp | `Date` header | RFC 2822 format |
| `encodingId` | Subject line | Must be `changeset-001` |
| `captureSystemId` | Message body | UUID of capture system instance |

### Content Types

Content type is determined by file extension per [capture-types.md](capture-types.md). A single message may contain multiple content types when multiple files are changed.

### captureContext

Not applicable. This encoding omits processing confirmation (requirement 10), so `captureContext` round-tripping is unnecessary.
