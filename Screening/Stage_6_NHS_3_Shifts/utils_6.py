# utils_6.py — Stage 6 helpers: NHS Three Shifts (with main_shift)

import json
from typing import Dict, Any, Optional, List

ALLOWED = {"community": "Community", "digital": "Digital", "prevention": "Prevention"}

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
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

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    import re

    CUES = {
        "Community": [
            r"\bcommunity\b", r"\bprimary care\b", r"\bpharmacy\b", r"\bout[- ]of[- ]hospital\b",
            r"\bneighbourhood\b", r"\bintegrated care\b", r"\bhome[- ]based\b", r"\bambulatory\b"
        ],
        "Digital": [
            r"\bdigital\b", r"\bapp\b", r"\btele(medicine|health)\b", r"\bremote monitoring\b",
            r"\b(virtual ward|e[- ]?health|m[- ]?health)\b", r"\bAI\b", r"\bmachine learning\b",
            r"\belectronic (record|health record)\b"
        ],
        "Prevention": [
            r"\bprevent(ion|ive|ing)?\b", r"\b(prophylaxis|prophylactic)\b", r"\bscreen(ing|ed)\b",
            r"\bvaccin(e|ation|ated)\b", r"\brisk reduction\b", r"\bearly detection\b",
            r"\bpre(operative|operative)\b.*\b(beta[- ]blocker|statin|antibiotic|thromboprophylaxis)\b",
            r"\bfluoride\b", r"\bchemoprevent(ion|ive)\b", r"\brelapse prevention\b", r"\bre[- ]admission prevention\b"
        ]
    }

    def find_hits(text: str, pats):
        if not text:
            return []
        low = text.lower()
        hits = []
        for p in pats:
            if re.search(p, low):
                hits.append(p)
        # shorten to a few
        return hits[:6]

    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")
    if abstract:
        lines.append("Abstract:")
        lines.append(str(abstract)[:4000])

        # add cue hints
        cue_summary = {}
        for lab, pats in CUES.items():
            hits = find_hits(abstract, pats)
            if hits:
                cue_summary[lab] = len(hits)
        if cue_summary:
            lines.append(f"\nDetected shift cue counts (heuristic): {cue_summary}")

    lines.append(
        "\nTASK: Decide if the study aligns with NHS Three Shifts and identify the single MAIN shift. "
        "Return STRICT JSON per schema."
    )
    return "\n".join(lines)


def _norm_shift_one(s: Any) -> Optional[str]:
    if not s:
        return None
    low = str(s).strip().lower()
    for k, label in ALLOWED.items():
        if k in low:
            return label
    return None

def _norm_shift_list(vals: Any) -> List[str]:
    if not vals:
        return []
    if isinstance(vals, str):
        vals = [vals]
    out: List[str] = []
    for v in vals:
        lab = _norm_shift_one(v)
        if lab and lab not in out:
            out.append(lab)
    return out

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, v))

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]

    # Normalise shifts_detected
    shifts = _norm_shift_list(obj.get("shifts_detected", []))

    # Normalise main_shift; if missing but shifts exist, choose first listed
    main_shift = _norm_shift_one(obj.get("main_shift", None))
    if main_shift is None and shifts:
        main_shift = shifts[0]
    if main_shift is None:
        main_shift = "None"

    # Guardrails: if no shifts, force exclude and main_shift=None/None
    if not shifts:
        include = False
        main_shift = "None"

    confidence = _clamp_conf(obj.get("confidence", 0.0))

    return {
        "include_stage6": include,
        "reason_stage6": reason,
        "main_shift": main_shift,
        "shifts_detected": "; ".join(shifts),
        "confidence_stage6": confidence,
    }
