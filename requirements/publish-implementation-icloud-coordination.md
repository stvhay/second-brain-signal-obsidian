# Publish - iCloud Coordination

## Description

This document defines coordination requirements for systems sharing the iCloud Obsidian vault directory. When iCloud is used for both capture (edits coming in) and publish (content going out), both systems must coordinate to avoid conflicts.

## Purpose

Minimize conflicts when the same directory serves as:
- **Capture source:** User edits in Obsidian sync via iCloud, detected by fsnotify
- **Publish destination:** Processed content rsynced from Storage to iCloud

## Applicable Systems

- [capture-implementation-icloud-worktree.md](capture-implementation-icloud-worktree.md)
- [publish-implementation-icloud.md](publish-implementation-icloud.md)

## Deployment Constraints

1. The capture and publish iCloud implementations MUST be deployed together. You cannot use one without the other.

## Coordination Mechanism

**Principle:** Publish waits for user to finish editing before writing to iCloud.

**Quiet period detection:**
Per [calc-sync-wait-time.md](design-basis/calc-sync-wait-time.md), the system achieves 99% confidence that editing has stopped after 16 minutes of no observed edits.

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `quietPeriodMinutes` | 16 | 99% confidence user stopped editing (see design basis) |

**Observable signal:** Last modification timestamp in the iCloud vault directory.

**Rule:** Publish SHALL NOT begin rsync until `quietPeriodMinutes` have elapsed since the last observed filesystem change in `icloudVaultPath`.

## Publish Gating Behavior

**When Storage changes and publish is triggered:**

1. Check time since last filesystem change in `icloudVaultPath`
2. If < 16 minutes: queue the publish, wait for quiet period
3. If ≥ 16 minutes: proceed with rsync

**Queuing behavior:**

| Scenario | Behavior |
|----------|----------|
| Publish triggered during active editing | Wait for quiet period, then publish |
| Multiple Storage changes during wait | Coalesce into single publish (rsync copies current state) |
| Editing resumes during wait | Reset the 16-minute timer |

**Configuration:**

| Parameter | Description |
|-----------|-------------|
| `quietPeriodMinutes` | Minutes of silence before publish proceeds (default: 16) |
| `maxWaitMinutes` | Maximum time to wait before writing timeout status (default: 120) |

**Status file:** `.publish-status` in `icloudVaultPath`

If `maxWaitMinutes` is exceeded (continuous editing for over two hours), the system writes a timeout status to `.publish-status` rather than publishing. The Processing system is responsible for monitoring this file and notifying the user.

## Conflict Resolution

Despite coordination, conflicts remain possible (e.g., user resumes editing just as rsync starts).

**Conflict scenario:** Publish writes file X while user edits file X in Obsidian.

**Resolution policy:** User edits win.

| Situation | Outcome |
|-----------|---------|
| rsync overwrites user edit | User's edit syncs back via iCloud; capture detects it; Processing re-evaluates |
| iCloud conflict file created | User resolves manually; capture detects resolution |

**Rationale:** The capture path ensures no user work is lost. Even if publish overwrites a file, the user's version was already captured (or will be on next sync). The system eventually converges to the correct state.

**Invariant:** User edits are never permanently lost. They either:
1. Arrive via capture before publish runs, or
2. Arrive via capture after publish overwrites, triggering reprocessing

## Functional Requirements

1. [ICLOUD-COORD-001] The publish system SHALL NOT write to `icloudVaultPath` until `quietPeriodMinutes` have elapsed since the last filesystem change.

2. [ICLOUD-COORD-002] The publish system SHALL reset the quiet period timer when new filesystem changes are detected.

3. [ICLOUD-COORD-003] If `maxWaitMinutes` is exceeded without achieving a quiet period, the publish system SHALL write a timeout status to `.publish-status` in `icloudVaultPath`.

4. [ICLOUD-COORD-004] Both systems SHALL use the same `icloudVaultPath` configuration value.

5. [ICLOUD-COORD-005] User edits SHALL take precedence in conflict resolution; overwritten edits are recaptured and reprocessed.

6. [ICLOUD-COORD-006] If the last modification timestamp cannot be determined, the publish system SHALL assume editing is in progress and defer publish until the timestamp becomes readable.

7. [ICLOUD-COORD-007] The capture system SHALL update the last modification timestamp in `icloudVaultPath` when filesystem changes are detected, ensuring the observable signal is reliably produced.

8. [ICLOUD-COORD-008] RESERVED — Race condition mitigation between rsync and concurrent edits. Requires investigation of iCloud and rclone implementation details.

## Traceability

| Implementation Requirement | Implements |
|---------------------------|------------|
| ICLOUD-COORD-003 | PUB-008 (status exposure) |
| Processing monitors `.publish-status` | PROC-058, PROC-059, PROC-060 |

## Cross-Cutting Requirements

See [general.md](general.md) for logging, configuration, security, and error handling requirements.

## References

- [calc-sync-wait-time.md](design-basis/calc-sync-wait-time.md) — Design basis for 16-minute quiet period
- [capture-implementation-icloud-worktree.md](capture-implementation-icloud-worktree.md) — Capture implementation
- [publish-implementation-icloud.md](publish-implementation-icloud.md) — Publish implementation
