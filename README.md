# AI-Assisted Evidence Screening Pipeline  
*A governed, multi-stage framework for scalable NHS-aligned evidence review.*

---

## Executive Summary

This repository contains a structured, auditable seven-stage screening pipeline designed to reduce large evidence sets to strategically relevant, financially meaningful studies.

The framework was developed, validated, and then scaled using identical predefined inclusion rules.

### Validation Phase  
The pipeline was validated against a manually screened benchmark dataset of:

**361 studies**

Each stage was compared against human review using structured performance metrics (accuracy, precision, TP/TN/FP/FN).

### Full Deployment  
Following validation, the identical pipeline was applied to the full reference database of:

**5,175 references**

The AI-assisted pipeline reduced this to:

**186 high-value studies aligned with predefined criteria**

This represents:

- **4,989 records removed**
- **>95% workload reduction at the screening stage**

This is not autonomous AI decision-making.  
It is rule-based screening at scale — governed, validated, and auditable.

---

## The Problem

Systematic evidence screening is resource-intensive. As reference volumes increase:

- Manual screening becomes cognitively demanding.
- Reviewer consistency becomes harder to maintain.
- Scaling introduces operational risk.

At the same time, ungoverned AI use introduces different risks:

- Hallucinated reasoning
- Inconsistent outputs
- Lack of auditability
- Overconfident automation

This framework addresses both problems.

It operationalises **explicit, human-defined criteria** across seven structured stages, reducing workload while preserving transparency and validation.

---

## Pipeline Overview

The framework applies progressively narrower filters:

| Stage | Focus | Validation In | Validation Out | Accuracy |
|-------|-------|---------------|----------------|----------|
| 1 | Language & Publication Window | 361 | 358 | 99.2% |
| 2 | UK Setting | 358 | 295 | 83.2% |
| 3 | Health & Care Context | 295 | 270 | 93.2% |
| 4 | Publication Type & Integrity | 270 | 236 | 95.6% |
| 5 | Comparator + Impact Evidence | 236 | 166 | 78.4% |
| 6 | NHS Three Shifts Alignment | 166 | 71 | 77.7% |
| 7 | Cash-Releasing Savings | 71 | 16 | 84.5% |

Early stages apply structural eligibility filters.  
Middle stages introduce contextual and methodological criteria.  
Later stages apply strategic and fiscal relevance constraints.

The result is a sharply narrowed evidence base aligned to NHS transformation and financial impact priorities.

---

## Scaling & Operational Impact

Following validation on the 361-study benchmark dataset, the identical pipeline configuration was deployed across the full reference database (5,175 records).

**Full-scale results:**

- Initial database: 5,175 references  
- Retained after full pipeline: 186 studies  
- Reduction: 4,989 records removed  
- Workload reduction: >95%

Importantly, the same rule definitions used during validation were used during full deployment. No inclusion criteria were altered during scaling.

This demonstrates that structured AI-assisted screening can:

- Apply predefined criteria consistently at scale  
- Substantially reduce manual burden  
- Retain alignment with strategic and fiscal objectives  
- Maintain auditability and governance integrity  

---

## Design Principles

This pipeline is built on the following principles:

- **Human-defined inclusion rules** at every stage.
- **Strict JSON schema outputs** for deterministic parsing.
- **Stage-wise validation** against manual review.
- **Conservative handling of ambiguity.**
- **Explicit guardrails** to reduce false positives.
- **Full audit trail retention** for transparency.
- **Composable stage architecture** (each stage independently runnable).

AI is used to apply rules consistently — not to invent criteria.

---

## Validation & Performance

Validation was conducted at every stage using:

- True Positives (TP)
- True Negatives (TN)
- False Positives (FP)
- False Negatives (FN)
- Accuracy
- Precision

Performance trends reflect increasing conceptual complexity:

- Structural filters (Stages 1–4) show high agreement with manual review.
- Comparative and impact detection (Stage 5) introduces abstraction complexity.
- Strategic alignment mapping (Stage 6) requires interpretive judgement.
- Explicit financial detection (Stage 7) depends on clear fiscal phrasing.

Lower precision in later stages reflects the difficulty of detecting nuanced signals within abstracts — not uncontrolled AI behaviour.

All outputs are retained for manual audit and reconciliation.

---

## Governance & Safeguards

This framework is designed for supervised deployment.

Key safeguards include:

- No autonomous final decision-making.
- Conservative exclusion logic.
- Explicit ambiguity handling.
- Strict output schema enforcement.
- Validation against human screening.
- Manual adjudication opportunities at later stages.

This is a decision-support tool — not a replacement for expert review.

---

## What This Is Not

- Not a fully automated systematic review engine.
- Not a meta-analysis tool.
- Not a critical appraisal substitute.
- Not production-deployed decision support software.

It is a structured screening accelerator.

---

## Repository Structure

stage_01/ – Language & date eligibility
stage_02/ – UK setting filter
stage_03/ – Health & care context filter
stage_04/ – Publication type integrity
stage_05/ – Comparator & impact evidence
stage_06/ – NHS Three Shifts alignment
stage_07/ – Cash-releasing savings detection

Each stage contains:

- Prompt definition
- Processing script
- Validation results
- README documenting criteria and performance

Stages can be run independently or sequentially.

---

## Example Use Cases

- Rapid horizon scanning
- Policy-aligned evidence filtering
- Identification of cash-releasing interventions
- Strategic transformation evidence mapping
- Economic impact review preparation

---

## Limitations

- Classification is based on abstract-level information.
- Comparator and outcome signals may be implicit rather than explicit.
- Strategic alignment may require contextual interpretation.
- Financial savings detection depends on explicit terminology.
- Manual oversight remains essential.

## Repository Structure
