#!/usr/bin/env python3
# main_5.py — Stage 5: Uses comparison group AND measures primary cost/impact outcomes

import os
import sys
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_5 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage5_comparator_outcomes.csv"
DEFAULT_SYSTEM = "system_prompt_5.txt"
DEFAULT_MODEL = "gpt-4o"


def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _retry_api(client, system_prompt, user_prompt, model, max_retries=3, backoff=2.0):
    """
    Simple retry wrapper with exponential backoff.
    Returns raw string response (or a JSON string with an error payload on total failure).
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            return call_gpt_api(client, system_prompt, user_prompt, model=model)
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(backoff ** attempt)
            else:
                # Return a JSON-looking string your parser can handle
                return (
                    '{"include": false, "reason": "api_error: ' + str(e).replace('"', "'") +
                    '", "has_comparator": false, "detected_comparator": "Unknown", '
                    '"has_primary_outcomes": false, "detected_outcomes": [], "confidence": 0.0}'
                )


def main():
    parser = argparse.ArgumentParser(
        description="Stage 5 screening: comparator present AND primary outcomes (cost/impact) measured"
    )
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to input CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to output CSV")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="Path to system prompt text file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay (seconds) between API calls")
    parser.add_argument("--debug", action="store_true", help="Store model raw JSON and full prompt")
    parser.add_argument(
        "--progress-every", type=int, default=25,
        help="Print a plain progress line every N rows"
    )
    args = parser.parse_args()

    # Ensure unbuffered/line-buffered stdout so progress appears live
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    # Load data
    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit).copy()

    total = len(df)
    if total == 0:
        print("⚠️ No rows to process.", flush=True)
        return

    # Prep prompt + API client
    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    rows = []

    # Iterate with simple progress prints
    for i, (idx, row) in enumerate(df.iterrows(), start=1):
        uid = row["id"]
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")
        # Pass all row fields as metadata (utils will pick only hint keys)
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        user_prompt = build_user_prompt(uid, title, abstract, metadata)
        raw = _retry_api(client, system_prompt, user_prompt, model=args.model)

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["id"] = uid

        if args.debug:
            # Keep the full prompt & raw model output for auditability
            normalized["stage5_prompt"] = user_prompt
            normalized["stage5_raw_json"] = raw

        rows.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

        # Progress print
        if args.progress_every and (i % args.progress_every == 0 or i == 1 or i == total):
            print(f"[PROGRESS] {i}/{total} (last id={uid})", flush=True)

    # Merge results back to input
    res = pd.DataFrame(rows)
    out = df.merge(res, on="id", how="left")

    # Save
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"Stage 5 screening complete. Wrote: {args.output}", flush=True)


if __name__ == "__main__":
    main()
