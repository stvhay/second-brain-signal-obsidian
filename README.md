# Second Brain

A personal knowledge capture system using Signal as the frontend and Obsidian as storage. Based on [Nate B Jones' "8 Building Blocks" architecture](https://www.youtube.com/watch?v=0TpON5T-Sw4).

Send notes to yourself via Signal. Claude classifies and files them in your Obsidian vault, then commits to git. Your Mac receives an MQTT notification, pulls the changes, and syncs to Obsidian via iCloud.

## Architecture

![Overview](diagrams/00-overview.svg)

| Stage | Diagram | Description |
|-------|---------|-------------|
| [Capture](diagrams/01-capture.svg) | ![Capture](diagrams/01-capture.svg) | iOS Shortcuts & Signal → signal-cli daemon |
| [Process](diagrams/02-process.svg) | ![Process](diagrams/02-process.svg) | receipt → classify → form → bounce |
| [Storage](diagrams/03-storage.svg) | ![Storage](diagrams/03-storage.svg) | Obsidian vault → git hook |
| [Publish](diagrams/04-publish.svg) | ![Publish](diagrams/04-publish.svg) | MQTT → launchctl service → iCloud |

For detailed specifications, see [`requirements/`](requirements/).

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

I use both daily. Signal handles delivery, encryption, and attachments. Obsidian stores everything as local markdown I control.

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

## Open Ideas

- Use ```rclone``` to mount and bidirectionally sync iCloud?
    - ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Testcloud/.obsidian

## Status

**Current state:** Capture system specified; Processing in design

- [x] signal-cli receiving messages via REST API
- [x] Capture system requirements complete
- [x] Message encoding format defined (`messaging-001`)
- [ ] Processing system implementation (claude brain-processor)
- [ ] MQTT notification layer
- [ ] Mac sync daemon
- [ ] Digest and fix flows
