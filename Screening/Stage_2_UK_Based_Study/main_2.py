#!/usr/bin/env python3
"""
Stage 2 screening: "Is a UK study or applied to a UK setting (incl. NHS / England / Wales / Scotland / NI)?"

This version prints simple progress lines like:
  [PROGRESS] 50/1200 (last id=J050)
so you can see where it is up to in PowerShell.

Usage (PowerShell):
  $env:PYTHONUNBUFFERED = "1"
  python -u .\main_2.py --input data/stage1.csv --output data/stage2.csv --progress-every 25
"""

import os
import sys
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_2 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/361_articles_post_stage1_screen.csv"
DEFAULT_OUTPUT = "data/screen_stage2_uk.csv"
DEFAULT_SYSTEM_PROMPT = "system_prompt_2.txt"
DEFAULT_MODEL = "gpt-4o"


def read_system_prompt(path: str) -> str:
    """Load the system prompt text that defines the screening rule & JSON schema."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    # ---- 1) CLI args ----
    parser = argparse.ArgumentParser(
        description="Stage 2 screening: UK study / applied to a UK setting"
    )
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to input CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to output CSV")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="Path to system prompt text file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay (seconds) between API calls")
    parser.add_argument("--progress-every", type=int, default=25,
                        help="Print a plain progress line every N rows")
    args = parser.parse_args()

    # ---- 2) Ensure unbuffered output for live progress ----
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    # ---- 3) Load data ----
    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit).copy()

    total = len(df)
    if total == 0:
        print("⚠️ No rows to process.", flush=True)
        return

    # ---- 4) Prep prompt + API client ----
    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    results = []

    # ---- 5) Iterate rows ----
    for i, (idx, row) in enumerate(df.iterrows(), start=1):
        uid = row["id"]
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")

        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        user_prompt = build_user_prompt(
            unique_id=uid,
            title=title,
            abstract=abstract,
            metadata=metadata
        )

        raw = call_gpt_api(
            client=client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=args.model
        )

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["id"] = uid

        results.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

        # ---- Progress print ----
        if args.progress_every and (i % args.progress_every == 0 or i == 1 or i == total):
            print(f"[PROGRESS] {i}/{total} (last id={uid})", flush=True)

    # ---- 6) Merge results back to input ----
    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="id", how="left")

    # ---- 7) Save ----
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"Stage 2 screening complete. Wrote: {args.output}", flush=True)


if __name__ == "__main__":
    main()
