import json
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Robustly parse JSON object from model output."""
    if not s:
        return None
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        # Try to extract {...}
        start, end = s.find("{"), s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                return None
    return None

def build_user_prompt(unique_id: str, year: Any, title: str, abstract: str) -> str:
    """Build user prompt for a single article row."""
    lines = []
    lines.append(f"ARTICLE ID: {id}")
    if year:
        lines.append(f"Declared year: {year}")
    if title:
        lines.append(f"Title: {title}")
    if abstract:
        lines.append(f"Abstract: {abstract}")  # cap length

    lines.append("\nTASK: Determine if the article is in English and published 2019–2025, return STRICT JSON per schema.")
    return "\n".join(lines)

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Standardize model output into safe fields."""
    return {
        "include_stage1": bool(obj.get("include", False)),
        "reason_stage1": str(obj.get("reason", ""))[:250],
        "detected_language": str(obj.get("detected_language", "Unknown")),
        "publication_year": obj.get("publication_year", None),
        "confidence_stage1": obj.get("confidence", 0.0)
    }
