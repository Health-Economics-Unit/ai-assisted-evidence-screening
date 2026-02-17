
# Stage 1 – Eligibility Gate: Language & Publication Window

## 1️. Stage Overview

Stage 1 is a metadata eligibility gate.

It does not assess topical relevance or study design. Instead, it ensures that only articles meeting two foundational criteria — language and publication window — progress further in the screening process.

This stage reduces administrative noise while preserving potentially relevant evidence for detailed review.

---

## 2️. Screening Objective

At this stage, the AI determines whether each record satisfies a single eligibility rule:

> Is the article written in English and published between 1 January 2019 and 31 December 2025 (inclusive)?

No other criteria are applied at this stage.

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF:

1. The article is written in English (primary language is English), AND  
2. The publication year is between 2019 and 2025 (inclusive).

### Publication Handling Rules:

- If multiple dates are present, the **latest explicit publication year** is used.
- “Online ahead of print” is not used unless it is the only publication date.
- Preprints count if posted within 2019–2025.
- Conference abstracts and posters count if dated within the window.

### Exclusion Rules:

- If the article is not in English → **Exclude**
- If publication year falls outside 2019–2025 → **Exclude**
- If language or year cannot be confidently determined → **Do NOT include**

Stage 1 is conservative in cases of uncertainty.

---

## 4️. Operational Logic

This stage uses a structured system prompt (`system_prompt_1.txt`) requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "detected_language": "English" | "Not English" | "Unknown",
  "publication_year": 2019 | 2020 | ... | 2025 | null,
  "confidence": 0.0-1.0
}
```

## Safeguards Built Into the Prompt

- Language must be clearly identifiable as English.
- Publication year must be explicitly determinable from metadata or text.
- Ambiguous cases default to exclusion.
- Reasons are capped at 20 words for audit clarity.
- No prose outside the JSON schema is permitted.
- All outputs are stored for direct comparison with manual review.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 361 |
| Included | 358 |
| Excluded | 3 |

Stage 1 retained **99.2%** of records for downstream review.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 358 |
| True Negatives (TN) | 0 |
| False Positives (FP) | 0 |
| False Negatives (FN) | 3 |
| Accuracy | 99.2% |
| Precision | 99.2% |

### Interpretation

- No records were incorrectly included.
- Only three records were not identified at this stage.
- The stage functioned as a high-sensitivity eligibility filter.

Given its role as an early gating mechanism, minimising inappropriate exclusion was prioritised.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding relevant studies due to ambiguous or incomplete metadata.

**Mitigation measures:**

- Conservative handling of uncertainty.
- Strict rule-based inclusion logic.
- Full validation against manual screening.

This stage is intentionally broad and low-risk.

---

## 8️. Role Within the Pipeline

Stage 1 ensures that all subsequent screening operates within:

- A defined publication window.
- A consistent language base.

This prevents later stages from expending analytical effort on administratively ineligible records.
