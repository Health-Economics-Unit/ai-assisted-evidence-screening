# utils_5.py — Stage 5 helpers: “Uses comparison group AND measures primary outcomes (cost/impact)”

import json
import re
from typing import Dict, Any, Optional, List

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly, falling back to the first {...} block."""
    if not s:
        return None
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        start, end = s.find("{"), s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                return None
    return None

HINT_KEYS = (
    "design","method","methods","study_type","trial","arm","arms",
    "comparator","control","intervention","outcomes","endpoint","endpoints",
    "primary_outcome","secondary_outcome","measure","metrics"
)

# ------- Lightweight cue finders (to help the model “see” implicit comparators / outcomes) -------

_COMPARATOR_CUES = {
    # Explicit
    r"\b(control|placebo|comparator|randomi[sz]ed|standard care|usual care|business as usual|BAU)\b": "explicit",
    r"\b(non[- ]inferiority|superiority|head[- ]to[- ]head|versus|vs\.?)\b": "explicit",
    # Implicit — time / pre-post with a defined change
    r"\b(pre[- ]?intervention|post[- ]?intervention|pre[- ]?implementation|post[- ]?implementation|baseline|before|after)\b": "pre_post",
    r"\b(increased|decreased|reduced|fell|rose|change(d)? by|from .* to)\b": "delta",
    # Implicit — switch/substitution
    r"\b(switch(ed|ing)?|transition(ed|ing)?|substitut(e|ion)|replace(d|ment))\b": "switch",
    # Implicit — scenario / counterfactual in modelling
    r"\b(counterfactual|do[- ]?nothing|status quo|current strategy|baseline scenario|no intervention)\b": "scenario",
    # Implicit — benchmark vs observed
    r"\b(expected|forecast(ed)?|predicted)\b.*\b(actual|observed)\b": "benchmark_vs_observed",
    # Implicit — technique/device head-to-head
    r"\b(first[- ]generation|second[- ]generation|technique [AB]|method [AB])\b": "technique"
}

_OUTCOME_CUES = {
    # Economics
    r"\b(cost(s)?|saving(s)?|budget|expenditure|tariff|price|ICER|QALY(s)?|ROI|net monetary benefit|NMB)\b": "cost",
    r"\b(QALY|utility|utilities|quality[- ]adjusted)\b": "qaly",
    # Service utilisation & time
    r"\b(utili[sz]ation|throughput|admission(s)?|readmission(s)?|attendance(s)?|uptake|hospitali[sz]ation(s)?)\b": "utilization",
    r"\b(length of stay|LOS|waiting time(s)?|time to|duration|turnaround time)\b": "time",
    # Clinical / detection / effectiveness (broadened)
    r"\b(mortality|morbidity|complication(s)?|effectiveness|efficacy|detection rate(s)?|remission|healing|hysterectomy|hba1c|glycated haemoglobin|weight loss|body mass index|bmi|fatigue)\b": "clinical",
    # Safety
    r"\b(adverse event(s)?|safety|harms?)\b": "safety",
    # PROs / HRQoL (QoL only here to avoid overlap with 'clinical')
    r"\b(PROs?|PROMs?|HRQoL|EQ-5D|HUI3|quality of life|qol)\b": "pro",
    # Workforce/retention
    r"\b(retention|turnover)\b": "impact"
}

def _find_cues(text: Any, patterns: Dict[str, str], max_hits: int = 8) -> List[str]:
    """Return a small set of cue labels present in text (case-insensitive). NaN-safe."""
    if not isinstance(text, str) or not text:
        return []
    hits = []
    low = text.lower()
    for pat, label in patterns.items():
        if re.search(pat, low):
            hits.append(label)
            if len(hits) >= max_hits:
                break
    # dedupe preserving order
    out = []
    for h in hits:
        if h not in out:
            out.append(h)
    return out

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

def build_user_prompt(unique_id: str, title: Any, abstract: Any, metadata: Dict[str, Any]) -> str:
    """Build user prompt emphasizing design/comparator/outcomes clues (explicit + implicit)."""
    # Coerce potential NaN/non-string inputs
    title = title if isinstance(title, str) else ""
    abstract = abstract if isinstance(abstract, str) else ""

    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")

    if metadata:
        hints = {k: str(metadata[k])[:200] for k in HINT_KEYS if k in metadata and metadata[k] not in (None, "")}
        if hints:
            lines.append(f"Potential design/outcome hints (raw metadata): {hints}")

    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

        # Surface detected cues to guide the model
        comp_cues = _find_cues(abstract, _COMPARATOR_CUES)
        out_cues = _find_cues(abstract, _OUTCOME_CUES)
        if comp_cues:
            lines.append(f"\nDetected comparator cues (incl. implicit): {sorted(set(comp_cues))}")
        if out_cues:
            lines.append(f"Detected outcome cues: {sorted(set(out_cues))}")

    # Comparator cheat-sheet aligned with Stage-5 system prompt
    lines.append(
        "\nCOMPARATOR CHECKLIST (A): Count explicit AND implicit comparators.\n"
        "- Explicit: usual/standard care, control/placebo, randomised arms, head-to-head (vs/versus).\n"
        "- Implicit: (1) pre-/post- with numeric deltas tied to a defined change; "
        "(2) switch/substitution (e.g., originator→biosimilar) with outcomes; "
        "(3) scenario/counterfactual modelling (baseline/status quo/do-nothing vs intervention); "
        "(4) expected/forecast vs actual/observed; "
        "(5) technique/device generations compared."
    )
    lines.append(
        "OUTCOME CHECKLIST (B): Primary outcomes on cost or impact (e.g., costs/savings, ICER/QALY/NMB, "
        "utilisation/readmissions/LOS/uptake/waiting time, clinical effectiveness/mortality/complications/detection, "
        "safety/adverse events, PROs/HRQoL, workforce retention/turnover)."
    )
    lines.append(
        "\nTASK: Decide if the study uses a comparison group AND measures primary cost/impact outcomes. "
        "If either is unclear, EXCLUDE. Return STRICT JSON per schema."
    )
    return "\n".join(lines)

# --- Normalization helpers ---

def _norm_bool(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    s = str(x).strip().lower()
    return s in {"true","1","yes","y"}

_COMPARATOR_MAP = {
    # explicit labels
    "usual": "Usual/Standard care", "standard": "Usual/Standard care", "usual care": "Usual/Standard care",
    "bau": "BAU", "business as usual": "BAU",
    "no intervention": "No intervention/Do nothing", "do nothing": "No intervention/Do nothing",
    "placebo": "Placebo",
    # generic
    "control": "Other", "comparator": "Other", "versus": "Other", "vs": "Other",
    # implicit signals we still normalize as 'Other'
    "baseline": "Other", "before": "Other", "after": "Other", "pre": "Other", "post": "Other",
    "switch": "Other", "switched": "Other", "transition": "Other", "counterfactual": "Other",
    "status quo": "Other", "current strategy": "Other", "expected": "Other", "observed": "Other",
    "first-generation": "Other", "second-generation": "Other", "head-to-head": "Other", "non-inferiority": "Other",
    "active": "Active comparator"
}

def _normalize_comparator(v: Any) -> str:
    if v is None:
        return "Unknown"
    s = str(v).lower()
    for k, mapped in _COMPARATOR_MAP.items():
        if k in s:
            return mapped
    return "Other" if s and s != "unknown" else "Unknown"

_ALLOWED_OUTCOMES = {"cost","qaly","clinical","utilization","time","safety","pro","impact","other"}

def _normalize_outcomes(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        items = [str(x).lower().strip() for x in v]
    else:
        items = [str(v).lower().strip()]
    # tokenize on commas if needed
    norm = []
    for item in items:
        for token in [t.strip() for t in item.split(",") if t.strip()]:
            norm.append(token)
    # map common synonyms
    mapped = []
    for t in norm:
        if "qaly" in t or "utility" in t or "quality-adjusted" in t:
            mapped.append("qaly")
        elif any(w in t for w in ["cost","economic","budget","icer","roi","nmb","tariff","price","saving"]):
            mapped.append("cost")
        elif any(w in t for w in ["readmission","admission","utilization","utilisation","throughput","use","attendance","uptake","hospitalisation","hospitalization"]):
            mapped.append("utilization")
        elif "length of stay" in t or "los" in t or re.search(r"\btime\b", t):
            mapped.append("time")
        elif any(w in t for w in ["mortality","morbidity","clinical","effectiveness","efficacy","detection rate","remission","healing","hysterectomy","hba1c","glycated haemoglobin","weight loss","body mass index","bmi","fatigue"]):
            mapped.append("clinical")
        elif any(w in t for w in ["safety","adverse","harm"]):
            mapped.append("safety")
        elif any(w in t for w in ["prom","pro","hrqol","quality of life","qol","eq-5d","hui3"]):
            mapped.append("pro")
        elif any(w in t for w in ["impact","effect","outcome","retention","turnover"]):
            mapped.append("impact")
        else:
            mapped.append("other")
    # keep only allowed, dedupe preserving order
    out = []
    for t in mapped:
        if t in _ALLOWED_OUTCOMES and t not in out:
            out.append(t)
    return out

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage-5 columns.
      include_stage5, reason_stage5, has_comparator, detected_comparator,
      has_primary_outcomes, detected_outcomes, confidence_stage5

    Safety: require BOTH has_comparator and has_primary_outcomes to be True; else include=False.
    Also: Option A — treat 'clinical' (and other recognized buckets) as impact:
          if detected_outcomes includes any allowed bucket (except 'other'), set has_primary_outcomes=True.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]

    has_comparator = _norm_bool(obj.get("has_comparator", False))
    detected_comparator = _normalize_comparator(obj.get("detected_comparator", "Unknown"))

    # Normalize outcomes list first
    detected_outcomes = _normalize_outcomes(obj.get("detected_outcomes", []))

    has_primary_outcomes = _norm_bool(obj.get("has_primary_outcomes", False))
    # --- Option A inference: if any meaningful bucket is present, force primary outcomes true
    if not has_primary_outcomes:
        if any(o in {"cost","qaly","clinical","utilization","time","safety","pro","impact"} for o in detected_outcomes):
            has_primary_outcomes = True

    confidence = _clamp_conf(obj.get("confidence", 0.0))

    # Final inclusion gate
    include = bool(has_comparator and has_primary_outcomes)

    return {
        "include_stage5": include,
        "reason_stage5": reason,
        "has_comparator": has_comparator,
        "detected_comparator": detected_comparator,
        "has_primary_outcomes": has_primary_outcomes,
        "detected_outcomes": detected_outcomes,
        "confidence_stage5": confidence,
    }
