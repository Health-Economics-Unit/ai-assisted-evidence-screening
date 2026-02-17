#!/usr/bin/env python3
"""
Stage 1 screening runner with plain progress output for PowerShell.

Prints lines like:
  [PROGRESS] 50/5176 (last id=ABC123)
so you always know how far it has got.
"""

import argparse
import os
import sys
import time
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_1 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/361_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage1.csv"
DEFAULT_SYSTEM_PROMPT = "system_prompt_1.txt"


def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 1 screening with plain progress lines.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--progress-every", type=int, default=25,
                        help="Print a progress line every N articles")
    args = parser.parse_args()

    # Make sure output flushes immediately
    try:
        sys.stdout.reconfigure(line_buffering=True)  # Python 3.7+
    except Exception:
        pass

    # Load input
    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit).copy()

    total = len(df)
    if total == 0:
        print("⚠️ No rows to process.", flush=True)
        return

    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    results = []
    for i, (idx, row) in enumerate(df.iterrows(), start=1):
        uid = row["id"]
        year = row.get("Year", "")
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")

        user_prompt = build_user_prompt(uid, year, title, abstract)
        raw = call_gpt_api(client, system_prompt, user_prompt, model=args.model)

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["id"] = uid
        results.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

        # Print progress line
        if args.progress_every and (i % args.progress_every == 0 or i == 1 or i == total):
            print(f"[PROGRESS] {i}/{total} (last id={uid})", flush=True)

    # Save
    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="id", how="left")
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    merged.to_csv(args.output, index=False)

    print(f" Stage 1 screening complete. Wrote: {args.output}", flush=True)


if __name__ == "__main__":
    main()
