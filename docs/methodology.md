# Methodology

This document explains the design logic behind the AI-assisted screening pipeline.

The framework was deliberately structured as a staged architecture — not a single composite prompt — to reflect how expert reviewers reason through large evidence bases.

It separates screening into distinct cognitive layers, validates each layer independently, and scales only after validation.

---

## Why Seven Stages?

Evidence screening naturally progresses through layered questions:

1. Administrative eligibility  
2. Geographic relevance  
3. Service context  
4. Publication integrity  
5. Comparative & impact evidence  
6. Strategic alignment  
7. Explicit fiscal impact  

Each stage isolates one decision boundary.

This design:

- Reduces cognitive overload  
- Improves traceability  
- Enables stage-level validation  
- Makes performance trade-offs visible  
- Preserves governance clarity  

A single multi-criteria classifier would obscure which rule drove inclusion or exclusion.  
The staged approach preserves transparency.

---

## Why This Order?

The order reflects increasing conceptual complexity.

**Stages 1–2: Structural filters**  
Objective, metadata-driven exclusions (language, date, UK setting).

**Stages 3–4: Context & integrity**  
Service environment and publication type.

**Stage 5: Methodological substance**  
Comparator detection and measurable impact.

**Stage 6: Strategic alignment**  
Mapping to NHS transformation priorities.

**Stage 7: Fiscal certainty**  
Explicit cash-releasing savings.

The progression moves from:

> “Is this eligible?”  
to  
> “Is this relevant?”  
to  
> “Is this strategically aligned?”  
to  
> “Does this release cash?”

Earlier removal of clearly ineligible records ensures later interpretive stages operate on a narrower, higher-quality evidence base.

Each layer increases abstraction.

By sequencing this way:

- Objective filters operate early.
- Interpretive judgement is applied only to narrowed datasets.
- Financial claims are assessed only after methodological and strategic relevance is confirmed.

This reduces noise and strengthens signal.

---

## Why Abstract-Level Screening?

The framework operates at abstract level because:

- Large-scale reviews begin before full-text access.
- Abstracts provide sufficient signals for early triage.
- Early-stage workload reduction produces disproportionate efficiency gains.

This framework accelerates narrowing prior to full-text review.  
It does not replace detailed appraisal.

---

## Validation Approach

Validation was conducted stage-by-stage against manual review on a benchmark dataset (361 studies).

This enabled:

- Transparent performance measurement  
- Guardrail refinement  
- Clear identification of abstraction boundaries  

The identical rule set was then deployed at scale across 5,175 references.  
No inclusion criteria were altered between validation and scaling.

---

## Conceptual Contribution

This framework demonstrates that AI-assisted screening can be:

- Modular  
- Governed  
- Auditable  
- Strategically aligned  
- Financially focused  

AI is used to apply predefined rules consistently — not to generate new criteria.

The result is structured acceleration, not automated judgement replacement.

---

## Intended Use

Appropriate for:

- Horizon scanning  
- Policy-aligned evidence mapping  
- Financial impact-focused reviews  
- Large-scale pre–full-text triage  

Not designed for:

- Full systematic review automation  
- Meta-analysis  
- Critical appraisal substitution  
- Clinical decision support  

Human oversight remains essential.
- Preserve governance at scale  

This is a framework, not a prompt.
