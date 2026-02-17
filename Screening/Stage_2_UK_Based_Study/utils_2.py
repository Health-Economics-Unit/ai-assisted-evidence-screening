# utils_2.py
# Helpers for Stage 2 screening: "Is a UK study or applied to a UK setting?"

import json
from typing import Dict, Any, Optional

# --- JSON parsing ---

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON from a model output string.

    - First try to parse the whole string as JSON.
    - If that fails, extract the first {...} block and parse that.
    - Return None if nothing valid is found.
    """
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


# --- Prompt building ---

UK_HINT_KEYS = (
    "country", "countries", "setting", "location", "region",
    "context", "dataset", "organisation", "organization", "affiliation"
)

def _shorten(value: Any, maxlen: int = 300) -> str:
    """Stringify and trim long metadata values for compact prompts."""
    if value is None:
        return ""
    s = str(value)
    return s if len(s) <= maxlen else s[:maxlen] + "…"

def build_user_prompt(
    unique_id: str,
    title: str,
    abstract: str,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Construct the user prompt for one article, surfacing any likely
    location/setting metadata to help the model decide UK vs Not UK.
    """
    lines = []
    lines.append(f"ARTICLE ID: {id}")
    if title:
        lines.append(f"Title: {title}")

    # Surface a few potentially relevant metadata fields (if present)
    if metadata:
        hints = {}
        for k in UK_HINT_KEYS:
            if k in metadata and metadata[k] not in (None, ""):
                hints[k] = _shorten(metadata[k])
        if hints:
            lines.append(f"Potential setting hints (raw metadata): {hints}")

    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

    # Task instruction aligned to system_prompt_2 (Criteria 2)
    lines.append(
        "\nTASK: Determine if the study is UK-based or applied to a UK setting "
        "(NHS, England, Wales, Scotland, Northern Ireland). "
        "Return STRICT JSON per schema."
    )
    return "\n".join(lines)


# --- Normalization ---

def _normalize_detected_setting(value: Any) -> str:
    """
    Map various model outputs to one of: 'UK', 'Not UK', 'Unknown'.
    """
    if value is None:
        return "Unknown"
    v = str(value).strip().lower()

    # Common synonyms the model might emit
    if v in {"uk", "united kingdom", "england", "wales", "scotland", "northern ireland", "nhs"}:
        return "UK"
    if v in {"not uk", "non-uk", "outside uk", "international (non-uk)", "no"}:
        return "Not UK"
    if "uk" in v or "england" in v or "wales" in v or "scotland" in v or "northern ireland" in v or "nhs" in v:
        # Any phrase containing a UK signal → UK
        return "UK"
    return "Unknown"

def _clamp_conf(p: Any) -> float:
    """Coerce confidence to float in [0, 1]."""
    try:
        x = float(p)
    except Exception:
        return 0.0
    return 0.0 if x < 0 else 1.0 if x > 1 else x

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize the model's JSON into Stage-2 fields.

    Returns keys:
      - include_stage2 (bool)
      - reason_stage2 (str, <=250 chars)
      - detected_setting (str: 'UK' | 'Not UK' | 'Unknown')
      - confidence_stage2 (float in [0,1])
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]
    detected_setting = _normalize_detected_setting(obj.get("detected_setting", "Unknown"))
    confidence = _clamp_conf(obj.get("confidence", 0.0))

    return {
        "include_stage2": include,
        "reason_stage2": reason,
        "detected_setting": detected_setting,
        "confidence_stage2": confidence,
    }





