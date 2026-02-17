# utils_7.py — Stage 7 helpers: “Explicit cash-releasing saving / positive ROI (STRICT PHRASES)”

import json
import re
from typing import Dict, Any, Optional, List

# -------------------- Robust JSON loader --------------------

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly, falling back to the first {...} block (if needed)."""
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

# -------------------- Cue detection (STRICT) --------------------
# NOTE: These cues are intentionally *narrow* to align with the Stage-7 prompt.
# We only surface cues that match the EXACTLY allowed inclusion phrases (plus minimal, safe variants).
# Anything that looks like generic “cost-effectiveness”, “ICER/QALY”, “ROI”, “efficiency”, or vague “cost reduction”
# is intentionally NOT captured here.

_CASH_SAVING_CUES = {
    # INCLUDE phrases (and minimal safe variants)
    r"\bin[- ]year cost saving(s)?\b": "in_year_cost_saving",
    r"\bin[- ]year negative net budget impact\b": "in_year_negative_net_budget_impact",
    r"\bnegative net budget impact\b": "negative_net_budget_impact",
    r"\bnet saving(s)?\b": "net_saving",
    r"\bexpenditure reduction(s)?\b": "expenditure_reduction",
    r"\bcash[- ]releasing saving(s)?\b": "cash_releasing_saving",
    r"\bbudget impact:\s*negative\b": "negative_budget_impact_colon_form",
    # “net benefit” is allowed per spec; restrict to avoid clinical “net benefit” by requiring nearby fiscal terms.
    # Two-part pattern: either the exact “net benefit” phrase with a money cue nearby, or explicit “net budget benefit”.
    r"(?:(?:net\s+benefit(?:s)?)\b(?:(?:(?!\n).){0,60})(?:£|\$|eur|euro|cost|budget|saving|expenditure|financial))": "net_benefit_with_money_cue",
    r"\bnet budget benefit(s)?\b": "net_budget_benefit",
}

_MONEY_CUES = re.compile(r"(£|\$|eur|euro|cost|budget|saving|expenditure|financial)", re.I)

def _find_cues(text: Any, patterns: Dict[str, str], max_hits: int = 12) -> List[str]:
    """Return a small set of cue labels present in text (case-insensitive). NaN-safe."""
    if not isinstance(text, str) or not text:
        return []
    hits: List[str] = []
    low = text.lower()
    for pat, label in patterns.items():
        try:
            if re.search(pat, low, flags=re.I | re.M):
                hits.append(label)
                if len(hits) >= max_hits:
                    break
        except re.error:
            continue
    # dedupe preserving order
    out: List[str] = []
    for h in hits:
        if h not in out:
            out.append(h)
    return out

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

# -------------------- Prompt builder --------------------

def build_user_prompt(unique_id: str, title: Any, abstract: Any, metadata: Dict[str, Any]) -> str:
    """
    Build the user prompt for Stage 7.
    STRICT: asks the model to judge inclusion ONLY when explicit cash-releasing saving / positive ROI phrases are present.
    """
    title = title if isinstance(title, str) else ""
    abstract = abstract if isinstance(abstract, str) else ""

    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")

    # Provide the abstract (shortened if huge)
    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

        # Surface detected STRICT cues to guide the model
        cues = _find_cues(abstract, _CASH_SAVING_CUES)
        if cues:
            lines.append(f"\nDetected cash-saving cues (STRICT): {sorted(set(cues))}")

    # Stage-7 rule recap + strict schema
    lines.append(
        "\nDECISION RULE (Stage 7): INCLUDE only if the article explicitly demonstrates "
        "cash-releasing savings or positive ROI with one of these outcomes stated clearly:\n"
        "- in-year cost saving\n"
        "- in-year negative net budget impact\n"
        "- negative net budget impact\n"
        "- net saving / net benefit\n"
        "- expenditure reduction\n"
        "- cash-releasing saving\n\n"
        "EXCLUDE if it only reports cost-effectiveness (ICER, QALY, ROI) without explicit savings; or only efficiency, utilisation, "
        "or clinical outcomes. If unclear or ambiguous, EXCLUDE."
    )
    lines.append(
        "\nReturn STRICT JSON only:\n"
        "{\n"
        '  \"include\": true | false,\n'
        '  \"reason\": \"short one-line justification\",\n'
        '  \"cash_saving_terms\": [\"net saving\",\"expenditure reduction\"] | [],\n'
        '  \"confidence\": 0.0-1.0\n'
        "}"
    )
    return "\n".join(lines)

# -------------------- Normalization --------------------

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

# Allowed internal labels (STRICT set)
_ALLOWED_TERM_LABELS = {
    "in_year_cost_saving",
    "in_year_negative_net_budget_impact",
    "negative_net_budget_impact",
    "net_saving",
    "expenditure_reduction",
    "cash_releasing_saving",
    "negative_budget_impact_colon_form",
    "net_benefit_with_money_cue",
    "net_budget_benefit",
}

_CANONICAL_TERM_MAP = {
    "in_year_cost_saving": "in-year cost saving",
    "in_year_negative_net_budget_impact": "in-year negative net budget impact",
    "negative_net_budget_impact": "negative net budget impact",
    "net_saving": "net saving",
    "expenditure_reduction": "expenditure reduction",
    "cash_releasing_saving": "cash-releasing saving",
    "negative_budget_impact_colon_form": "negative net budget impact",
    "net_benefit_with_money_cue": "net benefit",
    "net_budget_benefit": "net budget benefit",
}

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage-7 columns.
      include_stage7, reason_stage7, cash_saving_terms, confidence_stage7

    Safety: only accept include=True as provided by the model; we do NOT infer it.
    We still clamp confidence and sanitize terms to the STRICT set.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:240]

    terms_in = obj.get("cash_saving_terms", [])
    if isinstance(terms_in, str):
        terms_in = [terms_in]
    terms_norm: List[str] = []
    for t in terms_in or []:
        t_low = str(t).strip().lower()
        # If it's one of our internal labels, map to canonical phrase
        if t_low in _ALLOWED_TERM_LABELS:
            can = _CANONICAL_TERM_MAP.get(t_low, t_low)
            if can not in terms_norm:
                terms_norm.append(can)
        else:
            # Otherwise accept free-text ONLY if it matches one of the canonical phrases exactly.
            # This prevents leakage from generic terms like “cost reduction”, “cost-effective”, or “ROI”.
            t_ft = t_low
            if t_ft in {
                "in-year cost saving",
                "in year cost saving",
                "in-year negative net budget impact",
                "negative net budget impact",
                "net saving",
                "expenditure reduction",
                "cash-releasing saving",
                "cash releasing saving",
                "net benefit",
                "net budget benefit",
            } and t_ft not in terms_norm:
                terms_norm.append(t_ft)

    confidence = _clamp_conf(obj.get("confidence", 0.0))

    return {
        "include_stage7": include,
        "reason_stage7": reason,
        "cash_saving_terms": terms_norm,
        "confidence_stage7": confidence,
    }
