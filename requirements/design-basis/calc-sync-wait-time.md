# Engineering Calculation: Edit Session Timeout Inference

**Purpose:** Determine how long to wait after observing no edits before concluding (with high confidence) that a user has stopped editing.

**Date:** January 2026

---

## 1. Use Case

A note-taking application syncs user edits to a remote server. The system needs to detect when a user has transitioned from "actively editing" to "idle" in order to trigger downstream actions (e.g., finalizing a sync, releasing locks, updating status indicators).

The application auto-saves continuously during editing, with remote sync occurring approximately every minute. We observe a stream of sync events and must infer user state from the presence or absence of these events.

**Design goal:** Select a timeout interval such that if no edits are observed for that duration, we have ≥95% (or ≥99%) confidence the user has stopped editing.

---

## 2. Model

### 2.1 State Model

The user exists in one of two states:

- **Editing:** Actively working on a document. Edits (sync events) arrive as a Poisson process with rate S (edits/minute).
- **Not editing:** Idle. No edits occur (S = 0).

Session transitions are also modeled as Poisson processes:
- Users begin editing sessions at rate A (sessions/day)
- Editing sessions have average duration D (minutes)

### 2.2 Inference Problem

Given that we observed an edit at time t = 0 and have seen no edits for duration t, what is the probability the user is still editing?

This is a Bayesian inference problem. The posterior probability of still editing given silence of duration t is:

$$P(\text{editing} \mid \text{silence for } t) = \frac{e^{-(\lambda + S)t} \cdot (\lambda + S)}{\lambda + S \cdot e^{-(\lambda + S)t}}$$

where λ = 1/D is the rate of exiting the editing state.

### 2.3 Wait Time Formula

Solving for the time t required to achieve confidence level C (e.g., 0.95 or 0.99) that editing has stopped:

$$t_C = \frac{\ln\left(\frac{(1-C)}{C} \cdot \frac{S}{\lambda}\right)}{S + \lambda}$$

Since S >> λ in practice (many edits per session), this simplifies to:

$$t_C \approx \frac{\ln\left(\frac{1-C}{C} \cdot S \cdot D\right)}{S}$$

For 95% confidence: $t_{95\%} \approx \frac{\ln(19 \cdot S \cdot D)}{S}$

For 99% confidence: $t_{99\%} \approx \frac{\ln(99 \cdot S \cdot D)}{S}$

### 2.4 Parameter Sensitivity

| Parameter | Effect on wait time | Sensitivity |
|-----------|---------------------|-------------|
| S (edit rate) | Lower S → longer wait | ~Linear (appears in denominator) |
| D (session duration) | Higher D → longer wait | Logarithmic (dampened) |
| A (session frequency) | No effect | Only affects prior at random moments |

**Key insight:** The edit rate S dominates. A conservative (long) timeout requires assuming a slow editor, not necessarily a long session.

---

## 3. Parameters and Assumptions

### 3.1 Edit Rate Bound

The note-taking tool auto-saves during continuous editing, with remote sync every ~1 minute. However, users may pause to think, read, or context-switch without ending their session.

**Conservative assumption:** A user who is "still editing" makes at least one edit every 2 minutes on average.

$$S_{min} = 0.5 \text{ edits/minute}$$

This bounds the slowest editing behavior we expect to support without false-positive timeout.

### 3.2 Usage Modalities

We consider three representative editing patterns:

| Modality | Description | Session Frequency (A) | Session Duration (D) | Edit Rate (S) |
|----------|-------------|----------------------|---------------------|---------------|
| 1 | Quick note | Every 15 min | 1 min | 3/min |
| 2 | Regular session | Every 2 hours | 10 min | 0.5/min |
| 3 | Long project | Every 6 hours | 60 min | 0.5/min |

Modalities 2 and 3 use the conservative edit rate bound. Modality 1 represents rapid note-taking where edits are frequent.

---

## 4. Calculations

### 4.1 Modality 1: Quick Note

- S = 3/min, D = 1 min

$$t_{95\%} = \frac{\ln(19 \times 3 \times 1)}{3} = \frac{\ln(57)}{3} = \frac{4.04}{3} = 1.3 \text{ min}$$

$$t_{99\%} = \frac{\ln(99 \times 3 \times 1)}{3} = \frac{\ln(297)}{3} = \frac{5.69}{3} = 1.9 \text{ min}$$

### 4.2 Modality 2: Regular Session

- S = 0.5/min, D = 10 min

$$t_{95\%} = \frac{\ln(19 \times 0.5 \times 10)}{0.5} = \frac{\ln(95)}{0.5} = \frac{4.55}{0.5} = 9.1 \text{ min}$$

$$t_{99\%} = \frac{\ln(99 \times 0.5 \times 10)}{0.5} = \frac{\ln(495)}{0.5} = \frac{6.20}{0.5} = 12.4 \text{ min}$$

### 4.3 Modality 3: Long Project

- S = 0.5/min, D = 60 min

$$t_{95\%} = \frac{\ln(19 \times 0.5 \times 60)}{0.5} = \frac{\ln(570)}{0.5} = \frac{6.35}{0.5} = 12.7 \text{ min}$$

$$t_{99\%} = \frac{\ln(99 \times 0.5 \times 60)}{0.5} = \frac{\ln(2970)}{0.5} = \frac{8.00}{0.5} = 16.0 \text{ min}$$

---

## 5. Results Summary

| Modality | Description | 95% Confidence | 99% Confidence |
|----------|-------------|----------------|----------------|
| 1 | Quick note | 1.3 min | 1.9 min |
| 2 | Regular session | 9.1 min | 12.4 min |
| 3 | Long project | 12.7 min | 16.0 min |

The bounding case is Modality 3 (long project sessions with conservative edit rate).

---

## 6. Recommendation

**Recommended timeout: 16 minutes**

This provides 99% confidence that a user has stopped editing, even under conservative assumptions:

- Edit rate as low as 1 edit per 2 minutes
- Session duration up to 1 hour

For the more common quick-note and regular-session modalities, this threshold provides >99.9% confidence.

### Trade-offs

| Shorter timeout (e.g., 10 min) | Longer timeout (e.g., 20 min) |
|-------------------------------|------------------------------|
| Faster state detection | Higher confidence |
| Risk of false positives for slow editors | Delayed downstream actions |
| ~95% confidence for long sessions | Diminishing returns beyond 16 min |

### Implementation Notes

1. The 16-minute timeout applies from the *last observed edit*, not from session start.
2. Any observed edit resets the timer.
3. This analysis assumes edits are the only observable signal. If other activity indicators are available (e.g., cursor movement, document focus), they could be incorporated to reduce wait time.

---

## Appendix: Formula Derivation

Starting from Bayes' theorem, given we know the user was editing at t=0:

$$P(\text{editing at } t \mid \text{no edits in } [0,t]) = \frac{P(\text{no edits} \mid \text{editing throughout})P(\text{editing throughout})}{P(\text{no edits})}$$

The probability of no edits given continuous editing is $e^{-St}$ (Poisson).

The probability of still being in the editing state at time t (exponential duration model) is $e^{-\lambda t}$ where $\lambda = 1/D$.

Marginalizing over the transition time and solving yields the formula in Section 2.2.
