# Stage 7 – Cash-Releasing Savings Filter

## 1️. Stage Overview

Stage 7 represents the final and most restrictive filter in the pipeline.

At this stage, studies are retained only if they explicitly demonstrate cash-releasing savings or clear net budget reductions. This moves beyond cost-effectiveness or efficiency to focus solely on evidence showing direct financial savings.

This stage isolates studies that demonstrate immediate or explicit fiscal impact.

---

## 2️. Screening Objective

At this stage, the AI determines whether the article explicitly demonstrates:

> Clear cash-releasing savings or negative net budget impact.

Only studies that clearly state savings in financial terms are included.

Cost-effectiveness alone (e.g., ICERs, QALYs, ROI without savings) does not qualify.

---

## 3️. Inclusion Rule Applied

### INCLUDE only if the outcome explicitly states one of:

- In-year cost saving
- In-year negative net budget impact
- Negative net budget impact
- Net saving or net benefit
- Expenditure reduction
- Cash-releasing saving

### EXCLUDE if:

- Only cost-effectiveness is reported (e.g., ICER, QALY, ROI without explicit savings).
- Only efficiency, utilisation, or clinical outcomes are reported.
- Financial impact is unclear or ambiguous.

This stage requires explicit financial language indicating realised or projected savings.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "cash_saving_terms": ["net saving","expenditure reduction"] | [],
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Inclusion requires explicit mention of cash-releasing or net savings language.
- Cost-effectiveness metrics alone are insufficient.
- Efficiency gains without financial savings are excluded.
- Ambiguous financial statements result in exclusion.
- Reasons are limited to 20 words.
- No prose outside the JSON schema is permitted.
- All outputs are retained for validation and traceability.

This stage intentionally applies strict financial criteria to avoid overstating fiscal impact.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 71 |
| Included | 16 |
| Excluded | 55 |

Stage 7 reduced the dataset by approximately **77.5%**, isolating studies demonstrating explicit financial savings.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 14 |
| True Negatives (TN) | 46 |
| False Positives (FP) | 2 |
| False Negatives (FN) | 9 |
| Accuracy | 84.5% |
| Precision | 60.87% |

### Interpretation

- Accuracy remained strong at 84.5%, reflecting high overall agreement.
- False positives were low (2 records), indicating careful inclusion.
- Precision (60.87%) reflects the difficulty of detecting explicit savings language from abstracts alone.
- False negatives (9 records) suggest that some studies implied savings without using explicit financial terminology.

This stage is highly restrictive and dependent on clear financial phrasing within the abstract.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding studies where savings are implied but not explicitly stated in financial terms.

**Mitigation measures:**

- Strict requirement for explicit cash-saving terminology.
- Structured detection of recognised savings phrases.
- Validation against manual review.
- Opportunity for final manual adjudication.

Stage 7 prioritises financial certainty over breadth, accepting some sensitivity trade-off to ensure fiscal credibility.

---

## 8️. Role Within the Pipeline

Stage 7 isolates studies demonstrating direct cash-releasing savings.

After filtering for eligibility, contextual relevance, methodological integrity, comparative evidence, and strategic alignment, this final stage identifies evidence most directly relevant to immediate financial decision-making.

This marks the transition from strategic alignment to explicit fiscal impact.
