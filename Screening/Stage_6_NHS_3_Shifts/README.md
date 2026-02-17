# Stage 6 – NHS Three Shifts Alignment Filter

## 1️. Stage Overview

Stage 6 introduces strategic alignment filtering.

At this stage, studies are assessed to determine whether they align with at least one of the NHS “Three Shifts”:

- Hospital → Community
- Analogue → Digital
- Sickness → Prevention

Unlike earlier stages, which focused on eligibility, context, publication type, and comparative evidence, Stage 6 evaluates whether a study’s primary aim or intervention mechanism supports system-level transformation priorities.

This stage is inherently more interpretive and conceptually complex.

---

## 2️. Screening Objective

At this stage, the AI determines whether each study explicitly aligns with at least one of the NHS Three Shifts, and identifies the single main shift.

A study is included only if it clearly supports:

- Moving care from hospital to community settings,
- Replacing analogue processes with digital solutions, or
- Preventing illness or complications rather than reacting to established disease.

If alignment is unclear or ambiguous, the study is excluded.

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF the study explicitly relates to ≥1 of:

### 1️. Hospital → Community (“Community”)

- Explicit substitution of hospital or GP workload into community settings.
- Commissioning or implementation of new out-of-hospital services.
- Integrated, neighbourhood-based care models.

Does **not** include in-hospital efficiency improvements alone (e.g., ERAS pathways).

---

### 2️. Analogue → Digital (“Digital”)

- Digital solutions replacing or modernising analogue processes.
- Technologies reducing administrative burden or enabling coordinated care.
- Remote monitoring, virtual wards, automation, AI-driven systems.

Descriptive adoption audits without implementation or testing are excluded.

---

### 3️. Sickness → Prevention (“Prevention”)

The **primary aim** must be prevention of illness or complications.

Includes:

- Primary prevention (vaccination, health promotion)
- Secondary prevention (screening, risk stratification)
- Tertiary prevention (preventing complications or readmissions)

This is **setting-agnostic** — hospital-based prevention trials qualify if prevention is central.

---

### Exclude if:

- None of the Three Shifts clearly apply.
- Alignment is ambiguous or implied but not explicit.
- The study is descriptive, burden-focused, or utilisation-only without intervention.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "main_shift": "Community" | "Digital" | "Prevention" | "None",
  "shifts_detected": ["Community","Digital","Prevention"] | [],
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Exactly one `main_shift` must be selected if included.
- All applicable shifts are recorded in `shifts_detected`.
- If no clear alignment exists, `include=false`.
- Descriptive or economic burden studies without shift implementation are excluded.
- Treatment of established disease does not count as Prevention unless explicitly preventative.
- Reasons are limited to 20 words.
- No prose outside the JSON schema is permitted.
- All outputs are retained for validation and traceability.

This stage includes interpretive guardrails to reduce inappropriate strategic classification.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 166 |
| Included | 71 |
| Excluded | 95 |

Stage 6 reduced the dataset by approximately **57.2%**, concentrating the evidence base on studies aligned with NHS transformation priorities.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 34 |
| True Negatives (TN) | 46 |
| False Positives (FP) | 11 |
| False Negatives (FN) | 12 |
| Accuracy | 77.7% |
| Precision | 73.3% |

### Interpretation

- Precision decreased to 73.3%, reflecting the interpretive complexity of mapping abstracts to strategic policy shifts.
- False positives (11 records) indicate borderline strategic alignment.
- False negatives (12 records) reflect cases where alignment was implicit rather than explicitly articulated in abstracts.

This stage represents the most conceptually demanding classification layer in the pipeline.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Misclassifying studies due to strategic alignment being implicit rather than explicitly stated.

**Mitigation measures:**

- Clear definitions of each NHS shift.
- Requirement for explicit intervention or policy linkage.
- Structured selection of a single main shift.
- Full validation against manual review.
- Opportunity for manual adjudication in final stages.

Stage 6 is highly selective and interpretive, and therefore carries greater classification uncertainty than earlier structural filters.

---

## 8️. Role Within the Pipeline

Stage 6 aligns the evidence base with system transformation priorities.

After filtering for eligibility, context, publication integrity, and comparative impact, this stage ensures retained studies directly support one or more of the NHS Three Shifts.

This marks the transition from methodological relevance to strategic relevance.
