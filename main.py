import asyncio
import argparse
import json
import os
import time

from agent.main_agent import MainAgent
from engine.runner import BenchmarkRunner
from engine.retrieval_eval import RetrievalEvaluator
from engine.llm_judge import LLMJudge


# 🔧 CONFIG
CONFIG = {
    "TOP_K": 3,
    "STATUS_PASS_THRESHOLD_FINAL_SCORE": 3.0,
    "CONCURRENCY": 8
}


def load_dataset():
    path = "data/golden_set.jsonl"

    if not os.path.exists(path):
        raise FileNotFoundError("❌ Missing data/golden_set.jsonl")

    with open(path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        raise ValueError("❌ Dataset is empty")

    return dataset


async def run_version(dataset, version: str):
    print(f"\n🚀 Running benchmark for {version.upper()}")

    agent = MainAgent(version=version)
    evaluator = RetrievalEvaluator()
    judge = LLMJudge()

    runner = BenchmarkRunner(agent, evaluator, judge, CONFIG)

    start = time.time()
    results = await runner.run_all(dataset, concurrency=CONFIG["CONCURRENCY"])
    metrics = runner.aggregate_metrics(results)
    total_time = time.time() - start

    print(f"\n📊 {version.upper()} METRICS:")
    print(metrics)
    print(f"⏱ Total time: {total_time:.2f}s")

    return results, metrics


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="benchmark")
    parser.add_argument("--version", type=str, choices=["v1", "v2"])
    parser.add_argument("--both", action="store_true")

    args = parser.parse_args()

    dataset = load_dataset()

    v1_results, v2_results = None, None

    # 🔹 chạy 1 version
    if args.version:
        results, _ = await run_version(dataset, args.version)

        os.makedirs("reports", exist_ok=True)

        with open(f"reports/benchmark_{args.version}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return

    # 🔹 chạy cả 2
    if args.both:
        v1_results, _ = await run_version(dataset, "v1")
        v2_results, _ = await run_version(dataset, "v2")

    else:
        print("❌ Bạn phải chọn --version hoặc --both")
        return

    # 🔹 ghi file chuẩn
    os.makedirs("reports", exist_ok=True)

    final_output = {
        "v1_results": v1_results,
        "v2_results": v2_results
    }

    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("\n✅ Saved to reports/benchmark_results.json")


if __name__ == "__main__":
    asyncio.run(main())