# Stage 2 – UK Setting Eligibility Filter

## 1️. Stage Overview

Stage 2 introduces contextual relevance.

At this stage, articles are screened to determine whether they are conducted in, or directly applicable to, the United Kingdom. This ensures that subsequent stages focus on evidence relevant to UK health policy and service delivery.

Unlike Stage 1 (metadata gating), Stage 2 applies substantive contextual criteria. However, it remains deliberately conservative: when the study setting is unclear, records are retained and flagged for later review.

---

## 2️. Screening Objective

At this stage, the AI determines whether each record satisfies the following rule:

> Is the study conducted in the UK, or clearly applicable to a UK setting?

This includes studies referencing:

- United Kingdom
- UK
- England
- Wales
- Scotland
- Northern Ireland
- NHS
- UK-specific datasets, systems, or policies

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF:

1. The study is conducted in the UK, OR  
2. The study is explicitly applied to a UK setting.

### Additional Rules:

- If the study is international but includes the UK as a study site → Include.
- If the setting cannot be confidently determined → Include provisionally and mark as `"Unknown"`.

### EXCLUDE if:

- The study is clearly conducted outside the UK and not applicable to a UK context.

Stage 2 prioritises retention where ambiguity exists.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "detected_setting": "UK" | "Not UK" | "Unknown",
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Explicit geographic signals are required for confident UK classification.
- International multi-site studies including the UK are included.
- Unclear settings are marked `"Unknown"` and included provisionally.
- Reasons are limited to 20 words for audit clarity.
- No prose outside the JSON schema is permitted.
- All outputs are stored for validation and traceability.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 358 |
| Included | 295 |
| Excluded | 63 |

Stage 2 reduced the dataset by approximately **18%**, removing clearly non-UK studies.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 241 |
| True Negatives (TN) | 57 |
| False Positives (FP) | 54 (48 flagged) |
| False Negatives (FN) | 6 |
| Accuracy | 83.2% |
| Precision | 97.6% |

### Interpretation

- Precision remained very high (97.6%), meaning the vast majority of included studies were correctly identified.
- False negatives were low (6 records), minimising inappropriate exclusion.
- Many false positives (48 of 54) were provisionally included due to ambiguous setting and flagged for later review.

This reflects the intended design: when uncertain, retain rather than exclude.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding relevant UK studies due to incomplete or unclear location reporting.

**Mitigation measures:**

- Conservative inclusion of ambiguous cases.
- Explicit `"Unknown"` setting tagging.
- Manual review built into later stages.

Stage 2 is moderately selective but remains risk-aware and protective against premature exclusion.

---

## 8️. Role Within the Pipeline

Stage 2 narrows the evidence base to studies relevant to the UK health and policy context.

This ensures that subsequent stages — which may apply methodological or thematic filters — operate on a geographically relevant evidence pool.

By combining conservative logic with structured flagging, this stage balances efficiency with contextual accuracy.
