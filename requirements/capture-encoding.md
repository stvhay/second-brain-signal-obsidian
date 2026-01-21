# Capture Encoding Standards

## Encoding: `messaging-001`

This document defines the `messaging-001` encoding specification for capture messages.

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

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Unique message identifier |
| `encodingId` | string | Yes | Encoding specification identifier (e.g., `messaging-001`) |
| `captureSystemId` | UUID | Yes | Identifies the capture system instance |
| `timestamp` | string | Yes | ISO 8601 UTC timestamp (e.g., `2026-01-19T21:21:56.000Z`) |
| `location` | object | No | GPS coordinates if available |
| `content` | array | Yes | One or more content items |
| `captureContext` | object | No | Opaque object reserved for capture system use. Processing must include this unchanged in any response. |

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
