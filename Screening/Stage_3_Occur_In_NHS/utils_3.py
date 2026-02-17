# utils_3.py — Stage 3 helpers: “Occurs in NHS / health & social care / community health settings”

import json
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly (fallback to first {...} block)."""
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

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

# A few likely metadata keys to surface if present
HINT_KEYS = (
    "setting","location","context","service","care_level","site","country",
    "organisation","organization","provider","department"
)

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """Build the per-article user prompt emphasizing care setting clues."""
    lines = [f"ARTICLE ID: {unique_id}"]
    if title: lines.append(f"Title: {title}")

    if metadata:
        hints = {k: str(metadata[k])[:200] for k in HINT_KEYS if k in metadata and metadata[k] not in (None, "")}
        if hints:
            lines.append(f"Potential setting hints (raw metadata): {hints}")

    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

    lines.append(
        "\nTASK: Decide if the study occurs in NHS / Health & Social Care services / Community Health "
        "(incl. hospitals, primary care, clinics, patients' homes). Return STRICT JSON per schema."
    )
    return "\n".join(lines)

def _normalize_detected_context(v: Any) -> str:
    if v is None:
        return "Unknown"
    s = str(v).strip().lower()
    if "nhs" in s:
        return "NHS"
    if "social care" in s or "health & social care" in s or "health and social care" in s:
        return "Health & Social Care"
    if ("community" in s or "primary care" in s or "gp" in s or "clinic" in s or
        "outpatient" in s or "ambulatory" in s or "home" in s or "domiciliary" in s or "care home" in s or "hospital" in s):
        return "Community Health" if "nhs" not in s else "NHS"
    if "not" in s:
        return "Not applicable"
    return "Unknown"

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage 3 columns.
      include_stage3, reason_stage3, detected_context, confidence_stage3
    Safety: if detected_context is 'Not applicable' or 'Unknown', force include=False.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]
    detected_context = _normalize_detected_context(obj.get("detected_context", "Unknown"))
    confidence = _clamp_conf(obj.get("confidence", 0.0))

    if detected_context in {"Not applicable", "Unknown"}:
        include = False

    return {
        "include_stage3": include,
        "reason_stage3": reason,
        "detected_context": detected_context,
        "confidence_stage3": confidence,
    }
