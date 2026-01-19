# Second Brain

A personal knowledge capture system using Signal as the frontend and Obsidian as storage. Based on [Nate B Jones' "8 Building Blocks" architecture](https://www.youtube.com/watch?v=0TpON5T-Sw4).

Send notes to yourself via Signal. Claude classifies them, files them in your Obsidian vault, and commits to git. Your Mac gets notified via MQTT and pulls the changes into iCloud where Obsidian syncs automatically.

## Architecture

```
┌─────────────┐
│     iOS     │
│  Shortcuts  │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Signal    │────▶│  signal-cli  │────▶│ Claude          │
│ Note-to-Self│     │   daemon     │     │ brain-processor │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                    ┌──────────────┐              ▼
┌─────────────┐     │    MQTT      │     ┌─────────────────┐
│  Obsidian   │◀────│   notify     │◀────│   git commit    │
│  (iCloud)   │     └──────────────┘     │  (vault repo)   │
└─────────────┘              │           └─────────────────┘
       ▲                     ▼
       │            ┌──────────────┐
       └────────────│  Mac daemon  │
                    │  (git pull)  │
                    └──────────────┘
```

## The 8 Building Blocks

| Block | Purpose | Implementation |
|-------|---------|----------------|
| **Capture** | Quick input from anywhere | Signal Note-to-Self |
| **Sorter** | Classify and route notes | Claude agent |
| **Form** | Structured metadata | YAML frontmatter |
| **Filing Cabinet** | Organized storage | Obsidian folders |
| **Receipt** | Audit trail | `_inbox_log.md` |
| **Bouncer** | Hold low-confidence items | Confidence threshold |
| **Tap on Shoulder** | Scheduled summaries | Cron + Claude digest |
| **Fix Button** | Corrections | Signal reply ("fix: move X to People") |

## Why Signal + Obsidian

I already use both daily. Signal handles messaging complexity (delivery, encryption, attachments, voice memos) for free. Obsidian keeps everything in local markdown files I own.

## Planned Flows

### Capture → Classify → File

1. Send message to Signal Note-to-Self (text, voice memo, image, share sheet)
2. signal-cli daemon receives via JSON-RPC
3. Claude classifies: person, project, idea, task, admin
4. Files to appropriate Obsidian folder with YAML frontmatter
5. Commits to git, publishes MQTT notification
6. Mac daemon pulls, iCloud syncs to Obsidian

### Daily Digest

Cron triggers Claude at 7 AM to summarize active projects, recent captures, and pending tasks. Sends digest back via Signal.

### Fix Corrections

Reply to any note with "fix: move to Projects" or "fix: tag as urgent". Claude parses the correction, updates the vault, commits.

## Status

**Current state:** Design and prototyping

- [x] signal-cli receiving messages via REST API
- [ ] Claude brain-processor implementation
- [ ] MQTT notification layer
- [ ] Mac sync daemon
- [ ] Digest and fix flows
