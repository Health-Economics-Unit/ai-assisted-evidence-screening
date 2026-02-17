#!/usr/bin/env python3
# main_3.py — Stage 3: Occurs in NHS / health & social care / community health settings

import os
import sys
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_3 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage3_occurs_in_nhs.csv"
DEFAULT_SYSTEM = "system_prompt_3.txt"
DEFAULT_MODEL = "gpt-4o"


def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="Stage 3 screening: occurs in NHS / health & social care / community health settings"
    )
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to input CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to output CSV")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="Path to system prompt text file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay (seconds) between API calls")
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
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        user_prompt = build_user_prompt(uid, title, abstract, metadata)
        raw = call_gpt_api(client, system_prompt, user_prompt, model=args.model)

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["id"] = uid
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
    print(f"Stage 3 screening complete. Wrote: {args.output}", flush=True)


if __name__ == "__main__":
    main()
