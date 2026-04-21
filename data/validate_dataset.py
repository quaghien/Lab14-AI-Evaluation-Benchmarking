import argparse
import json
from pathlib import Path
from typing import Dict, List, Set

DATA_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = DATA_DIR / "chunks.jsonl"
GOLDEN_PATH = DATA_DIR / "golden_set.jsonl"
DEFAULT_EXPECTED = 50


def read_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path.as_posix()}")

    rows: List[Dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def run_validation(expected_total: int) -> int:
    chunks = read_jsonl(CHUNKS_PATH)
    golden = read_jsonl(GOLDEN_PATH)

    chunk_ids: Set[str] = {row["chunk_id"] for row in chunks if "chunk_id" in row}
    expected_ids = [row.get("expected_chunk_id", "") for row in golden]
    unique_expected_ids = set(expected_ids)

    status = 0

    if len(golden) == expected_total:
        print(f"PASS: total_records = {len(golden)}")
    else:
        print(f"FAIL: total_records = {len(golden)} (expected {expected_total})")
        status = 1

    if len(unique_expected_ids) == expected_total and len(expected_ids) == expected_total:
        print(f"PASS: unique_expected_chunk_ids = {len(unique_expected_ids)}")
    else:
        print(
            "FAIL: unique_expected_chunk_ids = "
            f"{len(unique_expected_ids)} (from {len(expected_ids)} records, expected {expected_total})"
        )
        status = 1

    missing_ids = [chunk_id for chunk_id in unique_expected_ids if chunk_id not in chunk_ids]
    if not missing_ids:
        print("PASS: all expected_chunk_id exist in chunks")
    else:
        print(f"FAIL: {len(missing_ids)} expected_chunk_id not found in chunks")
        status = 1

    return status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate chunk dataset and golden set.")
    parser.add_argument("--expected-total", type=int, default=DEFAULT_EXPECTED)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run_validation(args.expected_total))
