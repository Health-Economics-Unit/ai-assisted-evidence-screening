# Stage 5 – Comparative & Impact Evidence Filter

## 1️. Stage Overview

Stage 5 introduces a substantive methodological filter.

At this stage, studies are retained only if they both:

1. Use a comparator (explicit or implicit), AND  
2. Report primary outcomes on cost or measurable impact.

This stage represents a shift from contextual and publication filtering to identifying studies that generate comparative evidence relevant to economic evaluation and service impact.

---

## 2️. Screening Objective

At this stage, the AI determines whether each study satisfies the following rule:

> Does the study include a comparison group AND measure primary outcomes on cost or impact?

Both criteria must be satisfied for inclusion.

Studies that describe services, feasibility, audits, mapping/scoping reviews, or protocols without comparative quantitative outcomes are excluded.

---

## 3️. Inclusion Rule Applied

### INCLUDE if AND ONLY IF the study:

**A) Uses a comparator**, including:

- Usual or standard care
- Control or placebo
- No intervention / do nothing
- Business-as-usual (BAU)
- Active head-to-head comparison
- Pre/post intervention with numeric deltas
- Baseline vs intervention modelling
- Counterfactual scenarios
- Switch/substitution comparisons
- Observed vs expected contrasts

AND

**B) Measures primary outcomes on cost or impact**, including:

- Costs, savings, budget impact, ROI, ICER, QALY
- Clinical effectiveness (mortality, morbidity, complications)
- Service utilisation or throughput
- Length of stay or waiting time
- Safety or adverse events
- Patient-reported outcomes (PROs/HRQoL)
- Detection rates or functional outcomes

### Exclude if:

- No comparator is identifiable.
- No measurable cost or impact outcome is reported.
- The study is mapping/scoping, feasibility-only, narrative, audit, protocol, or descriptive without numeric comparative outcomes.

If either comparator or primary outcomes cannot be confidently determined from the abstract, the study is excluded.

---

## 4️. Operational Logic

This stage uses a structured system prompt requiring strict JSON output:

```json
{
  "include": true | false,
  "reason": "short one-line justification",
  "has_comparator": true | false,
  "detected_comparator": "Usual/Standard care" | "No intervention/Do nothing" | "Active comparator" | "Placebo" | "BAU" | "Other" | "Unknown",
  "has_primary_outcomes": true | false,
  "detected_outcomes": ["cost", "QALY", "clinical", "utilization", "time", "safety", "PRO", "impact", "other"],
  "confidence": 0.0-1.0
}
```
## Safeguards Built Into the Prompt

- Explicit and implicit comparator logic is defined.
- Narrative trends without counterfactuals do not qualify.
- Mapping/scoping reviews require explicit quantitative contrasts to qualify.
- Outcomes must include measurable cost or impact endpoints.
- Inclusion requires BOTH comparator and outcomes to be present.
- Reasons are limited to 20 words.
- No prose outside the JSON schema is permitted.
- All outputs are retained for validation and traceability.

This stage includes guardrails to reduce false positives from descriptive abstracts.

---

## 5️. Dataset Summary

| Metric | Value |
|--------|-------|
| Total Sample | 236 |
| Included | 166 |
| Excluded | 70 |

Stage 5 reduced the dataset by approximately **29.7%**, focusing the evidence base on studies generating comparative and outcome-based findings.

---

## 6️. Validation Against Manual Review

| Metric | Value |
|--------|-------|
| True Positives (TP) | 152 |
| True Negatives (TN) | 33 |
| False Positives (FP) | 14 |
| False Negatives (FN) | 37 |
| Accuracy | 78.4% |
| Precision | 80.4% |

### Interpretation

- Precision remained moderate at 80.4%, reflecting the complexity of detecting comparators and primary outcomes from abstracts.
- False negatives (37 records) indicate some comparative signals were not explicitly detectable in abstract text.
- False positives (14 records) reflect borderline cases where comparator or outcome signals were interpreted conservatively.

This stage represents a significant conceptual step change in difficulty compared to earlier structural filters.

---

## 7️. Risk Profile at This Stage

**Primary risk:**  
Excluding relevant comparative studies where the comparator or outcome is implied but not explicitly described in the abstract.

**Mitigation measures:**

- Explicit detection rules for both explicit and implicit comparators.
- Structured guardrails to prevent narrative-only inclusion.
- Full validation against manual review.
- Downstream opportunity for manual adjudication.

Stage 5 is intentionally more selective and carries higher classification complexity than earlier stages.

---

## 8️. Role Within the Pipeline

Stage 5 marks the transition from contextual and publication filtering to identifying analytically meaningful evidence.

By retaining only studies with comparators and measurable cost or impact outcomes, the pipeline concentrates on evidence capable of informing economic and service-level decision-making.

This stage significantly narrows the dataset to studies most relevant for economic evaluation and impact analysis.
