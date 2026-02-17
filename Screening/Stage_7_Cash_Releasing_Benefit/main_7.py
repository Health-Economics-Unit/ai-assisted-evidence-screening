#!/usr/bin/env python3
# main_7.py — Stage 7: Cash-Releasing Benefit

import os
import sys
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_7 import build_user_prompt, safe_json_loads, normalize_result


def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="Stage 7 screening: Cash-releasing savings / ROI evidence"
    )

    # Support both old and new flags
    parser.add_argument("--infile", "--input", dest="infile", required=True,
                        help="Input CSV file with articles")
    parser.add_argument("--outfile", "--output", dest="outfile", default="data/screen_stage7.csv",
                        help="Output CSV file for results")
    parser.add_argument("--id-col", default="id", help="Column name for unique article ID")
    parser.add_argument("--title-col", default="Title", help="Column name for article title")
    parser.add_argument("--abstract-col", default="Abstract", help="Column name for article abstract")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--system-prompt", default="system_prompt_7.txt", help="System prompt text file")
    parser.add_argument("--sample-n", type=int, default=None, help="Optional: only process first N rows")
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep interval between API calls")
    parser.add_argument("--dry-run", action="store_true", help="Run without calling API (for debugging)")
    parser.add_argument("--progress-every", type=int, default=25,
                        help="Print a plain progress line every N rows")

    args = parser.parse_args()

    # Ensure live progress in PowerShell/terminals
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    # Load input
    df = pd.read_csv(args.infile)
    if args.sample_n:
        df = df.head(args.sample_n).copy()

    total = len(df)
    if total == 0:
        print("⚠️ No rows to process.", flush=True)
        return

    system_prompt = read_system_prompt(args.system_prompt)
    client = create_openai_client()

    rows = []

    for i, (idx, row) in enumerate(df.iterrows(), start=1):
        uid = row.get(args.id_col, f"row_{idx}")
        title = row.get(args.title_col, "")
        abstract = row.get(args.abstract_col, "")
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        user_prompt = build_user_prompt(uid, title, abstract, metadata)

        if args.dry_run:
            raw = '{"include": false, "reason": "dry run", "cash_releasing": false, "confidence": 0.0}'
        else:
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

    res = pd.DataFrame(rows)
    out = df.merge(res, left_on=args.id_col, right_on="id", how="left")

    os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
    out.to_csv(args.outfile, index=False)
    print(f"Stage 7 screening complete. Wrote: {args.outfile}", flush=True)


if __name__ == "__main__":
    main()
