# Stage 4 – Publication Type & Quality Filter

## 1️. Stage Overview

Stage 4 introduces a publication integrity filter.

At this stage, articles are assessed to ensure they represent substantive research outputs rather than protocols, opinion pieces, or non-peer-reviewed publications. This stage strengthens methodological credibility by retaining peer-reviewed and recognised grey literature while removing publication types that do not contain evaluative findings.

Stage 4 represents a shift from contextual filtering (Stage 3) to research validity and publication quality assurance.

---

## 2️. Screening Objective

At this stage, the AI determines whether each record satisfies the following rule:

> Is the article a peer-reviewed study or recognised grey literature, and not a protocol, editorial, commentary, or predatory publication?

The objective is to retain substantive research outputs while removing non-empirical or low-integrity publication types.

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF:

1. The article is:
   - Peer-reviewed, OR
   - Recognised grey literature (e.g., reports, dissertations, conference abstracts), AND
2. It is NOT:
   - A study protocol,
   - An editorial or commentary,
   - Published in a predatory or non-peer-reviewed journal.

### Additional Rules:

- If publication type is unclear, classify as `"Unknown"` and include provisionally.
- Ambiguous cases are flagged for manual review.
- Explicit signals such as “study protocol”, “editorial”, “commentary”, or “opinion piece” trigger exclusion.

Stage 4 remains cautious when uncertainty exists but becomes more selective than earlier stages.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "publication_type": "Peer-reviewed" | "Grey literature" | "Protocol" | "Editorial/Commentary" | "Predatory/Non-peer-reviewed" | "Unknown",
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Explicit identification of protocols, editorials, and commentaries triggers exclusion.
- Grey literature is recognised and retained where appropriate.
- Predatory or non-peer-reviewed publications are excluded.
- Ambiguous publication types are marked `"Unknown"` and included provisionally.
- Reasons are limited to 20 words for audit clarity.
- No prose outside the JSON schema is permitted.
- All outputs are retained for validation and traceability.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 270 |
| Included | 236 |
| Excluded | 34 |

Stage 4 reduced the dataset by approximately **12.6%**, removing non-substantive or ineligible publication types.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 235 |
| True Negatives (TN) | 23 |
| False Positives (FP) | 1 |
| False Negatives (FN) | 11 |
| Accuracy | 95.6% |
| Precision | 95.5% |

### Interpretation

- Accuracy was high at 95.6%, indicating strong agreement with manual review.
- False positives were extremely low (1 record), demonstrating effective exclusion of inappropriate publication types.
- Some false negatives (11 records) reflect the challenge of detecting publication type reliably from abstracts alone.

Overall, Stage 4 demonstrated robust filtering of non-empirical publications while maintaining high concordance with manual screening.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding relevant empirical studies due to ambiguous publication type signals.

**Mitigation measures:**

- Conservative inclusion of `"Unknown"` publication types.
- Clear exclusion rules for explicitly identified protocols and editorials.
- Structured validation against manual review.

Stage 4 increases selectivity but remains governed and auditable.

---

## 8️. Role Within the Pipeline

Stage 4 ensures that downstream stages focus exclusively on substantive research outputs.

By removing protocols, editorials, commentaries, and predatory publications, the pipeline strengthens methodological integrity before applying more concept-specific or analytical filters.

This stage marks the transition from contextual relevance to research validity.
