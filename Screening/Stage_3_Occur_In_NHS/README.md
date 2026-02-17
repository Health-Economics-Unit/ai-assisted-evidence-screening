# Stage 3 – Health & Care Setting Filter

## 1️. Stage Overview

Stage 3 introduces a service-delivery context filter.

At this stage, articles are assessed to determine whether the study takes place within NHS, health and social care, or community health settings. This ensures that retained studies are grounded in real-world service environments rather than purely academic or laboratory contexts.

Unlike Stage 2 (geographic relevance), Stage 3 focuses on operational setting and service applicability.

---

## 2️. Screening Objective

At this stage, the AI determines whether each study occurs within a recognised health or care delivery environment.

The objective is to retain studies conducted in:

- NHS settings (any level of care)
- Health & Social Care services
- Community health settings

Studies outside direct health or care delivery contexts are excluded.

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF the study occurs in:

- NHS settings (any care level)
- Health & Social Care services
- Community health settings (e.g., hospitals, primary care/GP, outpatient clinics, community clinics, patients' homes, domiciliary care, care homes, home health)

### Exclude if:

- The setting is purely laboratory-based
- Simulation without clinical deployment
- Schools or workplaces without a health-service component
- The study setting cannot be confidently determined

If mixed settings are described, the study is included if any component occurs within an eligible health or care context.

Unclear settings are marked `"Unknown"` and excluded.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "detected_context": "NHS" | "Health & Social Care" | "Community Health" | "Not applicable" | "Unknown",
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Explicit service-delivery signals are required for confident inclusion.
- Mixed settings qualify if any component occurs within health or care delivery.
- Purely theoretical, laboratory, or non-clinical environments are excluded.
- Unclear contexts are marked `"Unknown"` and excluded.
- Reasons are limited to 20 words for audit clarity.
- No prose outside the JSON schema is permitted.
- All outputs are retained for validation and review.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 295 |
| Included | 270 |
| Excluded | 25 |

Stage 3 retained approximately **91.5%** of records from Stage 2, focusing the dataset on service-based evidence.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 267 |
| True Negatives (TN) | 8 |
| False Positives (FP) | 3 |
| False Negatives (FN) | 17 |
| Accuracy | 93.2% |
| Precision | 94% |

### Interpretation

- Precision remained strong at 94%, indicating that most included studies were correctly classified.
- False positives were low (3 records), demonstrating effective exclusion of non-service settings.
- Some false negatives (17 records) reflect the inherent difficulty of detecting service context from limited abstracts.

Overall, the stage demonstrated robust contextual filtering while maintaining high agreement with manual review.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding relevant studies where service context is implied but not explicitly described in the abstract.

**Mitigation measures:**

- Clear definition of eligible service settings.
- Inclusion of mixed-setting studies.
- Structured validation against manual review.

Stage 3 is more selective than earlier stages but remains governed and auditable.

---

## 8️. Role Within the Pipeline

Stage 3 ensures that subsequent screening focuses exclusively on evidence embedded in real-world health and care delivery environments.

By removing laboratory-only, simulation-only, and non-clinical contexts, the pipeline increasingly concentrates on studies with operational relevance to NHS and community services.

This marks the transition from broad contextual relevance to applied service evidence.

