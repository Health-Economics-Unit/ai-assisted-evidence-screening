# utils_4.py — Stage 4 helpers: “Peer-reviewed or grey literature (exclude protocols, editorials, predatory journals)”

import json
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON from model output (fallback to first {...} block)."""
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

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """Build the per-article user prompt with publication type context."""
    lines = [f"ARTICLE ID: {unique_id}"]
    if title: lines.append(f"Title: {title}")
    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))
    lines.append(
        "\nTASK: Determine if this is a peer-reviewed article or grey literature. "
        "Exclude protocols, editorials/commentaries, and predatory/non-peer-reviewed journals. "
        "Return STRICT JSON per schema."
    )
    return "\n".join(lines)

def _normalize_publication_type(v: Any) -> str:
    if v is None:
        return "Unknown"
    s = str(v).strip().lower()
    if "peer" in s:
        return "Peer-reviewed"
    if "grey" in s or "conference" in s or "dissertation" in s or "report" in s:
        return "Grey literature"
    if "protocol" in s:
        return "Protocol"
    if "editorial" in s or "commentary" in s or "opinion" in s:
        return "Editorial/Commentary"
    if "predatory" in s or "non-peer" in s or "non peer" in s:
        return "Predatory/Non-peer-reviewed"
    return "Unknown"

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage 4 columns.
      include_stage4, reason_stage4, publication_type, confidence_stage4
    Safety: if publication_type is Protocol / Editorial / Predatory / Unknown → include=False.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]
    publication_type = _normalize_publication_type(obj.get("publication_type", "Unknown"))
    confidence = _clamp_conf(obj.get("confidence", 0.0))

    if publication_type in {"Protocol", "Editorial/Commentary", "Predatory/Non-peer-reviewed"}:
        include = False

    return {
        "include_stage4": include,
        "reason_stage4": reason,
        "publication_type": publication_type,
        "confidence_stage4": confidence,
    }
