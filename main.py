import asyncio
import argparse
import json
import os
import time
from datetime import datetime, timezone

from agent.main_agent import MainAgent
from engine.runner import BenchmarkRunner
from engine.retrieval_eval import RetrievalEvaluator
from engine.llm_judge import LLMJudge


# 🔧 CONFIG
CONFIG = {
    "TOP_K": 3,
    "STATUS_PASS_THRESHOLD_FINAL_SCORE": 3.0,
    "CONCURRENCY": 8,
    "MAX_RETRY_PER_CASE": 1,
}
GATE_MIN_DELTA_HIT_RATE = 0.10
GATE_MIN_DELTA_MRR = 0.10
GATE_MIN_DELTA_FINAL_SCORE = 0.00


def load_dataset():
    path = "data/golden_set.jsonl"

    if not os.path.exists(path):
        raise FileNotFoundError("❌ Missing data/golden_set.jsonl")

    with open(path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        raise ValueError("❌ Dataset is empty")

    return dataset


def load_benchmark_results(path: str = "reports/benchmark_results.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Missing {path}. Run benchmark mode first.")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "v1_results" not in data or "v2_results" not in data:
        raise ValueError("❌ benchmark_results.json thiếu v1_results hoặc v2_results")
    return data


def aggregate_from_results(results):
    valid = [r for r in results if r.get("status") != "error"]
    if not valid:
        return {
            "hit_rate": 0.0,
            "mrr": 0.0,
            "avg_judge_score": 0.0,
            "avg_latency": 0.0,
            "pass_rate": 0.0,
            "valid_cases": 0,
            "error_cases": len(results),
        }

    return {
        "hit_rate": sum(r.get("hit_rate", 0.0) for r in valid) / len(valid),
        "mrr": sum(r.get("mrr", 0.0) for r in valid) / len(valid),
        "avg_judge_score": sum(r.get("final_score", 0.0) for r in valid) / len(valid),
        "avg_latency": sum(r.get("latency", 0.0) for r in valid) / len(valid),
        "pass_rate": sum(1 for r in valid if r.get("status") == "pass") / len(valid),
        "valid_cases": len(valid),
        "error_cases": len(results) - len(valid),
    }


def build_summary(benchmark_data):
    v1_results = benchmark_data["v1_results"]
    v2_results = benchmark_data["v2_results"]

    metrics_v1 = aggregate_from_results(v1_results)
    metrics_v2 = aggregate_from_results(v2_results)

    delta = {
        "delta_hit_rate": metrics_v2["hit_rate"] - metrics_v1["hit_rate"],
        "delta_mrr": metrics_v2["mrr"] - metrics_v1["mrr"],
        "delta_judge_score": metrics_v2["avg_judge_score"] - metrics_v1["avg_judge_score"],
        "delta_latency": metrics_v2["avg_latency"] - metrics_v1["avg_latency"],
    }

    conditions = {
        "hit_rate_non_decrease": metrics_v2["hit_rate"] >= metrics_v1["hit_rate"],
        "mrr_non_decrease": metrics_v2["mrr"] >= metrics_v1["mrr"],
        "delta_hit_rate_gte_0_10": delta["delta_hit_rate"] >= GATE_MIN_DELTA_HIT_RATE,
        "delta_mrr_gte_0_10": delta["delta_mrr"] >= GATE_MIN_DELTA_MRR,
        "delta_judge_score_gte_0_00": delta["delta_judge_score"] >= GATE_MIN_DELTA_FINAL_SCORE,
    }

    failed = [name for name, ok in conditions.items() if not ok]
    decision = "APPROVE" if not failed else "BLOCK RELEASE"
    reasons = ["All gate conditions passed."] if not failed else [f"Failed: {name}" for name in failed]

    summary = {
        "metadata": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "total_cases": max(len(v1_results), len(v2_results)),
        },
        "metrics_v1": metrics_v1,
        "metrics_v2": metrics_v2,
        "delta": delta,
        "release_decision": {
            "decision": decision,
            "reasons": reasons,
            "conditions": conditions,
        },
    }
    return summary


def write_failure_analysis(benchmark_data, summary, path="analysis/failure_analysis.md"):
    v1_results = benchmark_data["v1_results"]
    v2_results = benchmark_data["v2_results"]

    def is_miss(case):
        expected = case.get("expected_chunk_id")
        return expected not in (case.get("retrieved_chunk_ids") or [])

    v2_valid = [c for c in v2_results if c.get("status") != "error"]
    retrieval_miss = [c for c in v2_valid if is_miss(c)]
    low_judge = [c for c in v2_valid if c.get("final_score", 0) < 3.0]
    hallucination_like = [c for c in v2_valid if (not is_miss(c)) and c.get("final_score", 0) < 3.0]

    worst_cases = sorted(
        [c for c in v2_valid if c.get("status") == "fail"],
        key=lambda x: (x.get("final_score", 0), x.get("mrr", 1.0), x.get("hit_rate", 1.0))
    )[:5]

    lines = []
    lines.append("# Báo cáo Phân tích Thất bại (Failure Analysis Report)")
    lines.append("")
    lines.append("## 1. Tổng quan Benchmark")
    lines.append(f"- **Tổng số cases:** {summary['metadata']['total_cases']}")
    lines.append(f"- **V1:** hit_rate={summary['metrics_v1']['hit_rate']:.2f}, mrr={summary['metrics_v1']['mrr']:.2f}, avg_judge_score={summary['metrics_v1']['avg_judge_score']:.2f}")
    lines.append(f"- **V2:** hit_rate={summary['metrics_v2']['hit_rate']:.2f}, mrr={summary['metrics_v2']['mrr']:.2f}, avg_judge_score={summary['metrics_v2']['avg_judge_score']:.2f}")
    lines.append(f"- **Release decision:** {summary['release_decision']['decision']}")
    lines.append("")
    lines.append("## 2. Phân nhóm lỗi (Failure Clustering)")
    lines.append("| Nhóm lỗi | Số lượng | Mô tả |")
    lines.append("|---|---:|---|")
    lines.append(f"| Retrieval miss | {len(retrieval_miss)} | expected_chunk_id không nằm trong retrieved_chunk_ids |")
    lines.append(f"| Low judge score | {len(low_judge)} | final_score < 3.0 |")
    lines.append(f"| Hallucination-like | {len(hallucination_like)} | Retrieval hit nhưng điểm judge vẫn thấp |")
    lines.append("")
    lines.append("## 3. 5 Whys cho các case tệ nhất")

    if not worst_cases:
        lines.append("- Không có case fail trong V2.")
    else:
        for i, case in enumerate(worst_cases, 1):
            q = case.get("question", "")
            exp = case.get("expected_chunk_id")
            got = case.get("retrieved_chunk_ids", [])
            fs = case.get("final_score", 0)
            miss = exp not in (got or [])
            lines.append("")
            lines.append(f"### Case #{i}")
            lines.append(f"- **Question:** {q}")
            lines.append(f"- **Expected chunk:** `{exp}`")
            lines.append(f"- **Retrieved chunks:** `{got}`")
            lines.append(f"- **Scores:** hit_rate={case.get('hit_rate', 0):.2f}, mrr={case.get('mrr', 0):.2f}, final_score={fs:.2f}")
            if miss:
                lines.append("1. **Why 1:** Vì expected chunk không xuất hiện trong top-k.")
                lines.append("2. **Why 2:** Vì truy vấn và chunk có độ tương đồng ngữ nghĩa chưa đủ cao.")
                lines.append("3. **Why 3:** Vì chunking cố định làm phân mảnh thông tin quan trọng.")
                lines.append("4. **Why 4:** Vì chưa có bước reranking để sửa thứ tự kết quả gần đúng.")
                lines.append("5. **Why 5:** Vì chưa có cảnh báo tự động khi retrieval miss tăng đột biến.")
                lines.append("6. **Root Cause:** Retrieval quality chưa ổn định ở các câu mô tả quy định dài.")
            else:
                lines.append("1. **Why 1:** Vì expected chunk đã có nhưng điểm judge vẫn thấp.")
                lines.append("2. **Why 2:** Vì câu trả lời generation chưa trích đúng ý trong chunk.")
                lines.append("3. **Why 3:** Vì prompt trả lời chưa ép bám sát expected answer đủ mạnh.")
                lines.append("4. **Why 4:** Vì chưa có hậu kiểm nội dung trước khi trả lời cuối.")
                lines.append("5. **Why 5:** Vì chưa có test hồi quy theo nhóm câu dễ nhầm lẫn ngữ nghĩa gần.")
                lines.append("6. **Root Cause:** Generation/prompting chưa ổn định dù retrieval đã hit.")

    lines.append("")
    lines.append("## 4. Kế hoạch cải tiến (Action Plan)")
    lines.append("- [ ] Thêm reranker sau FAISS để cải thiện vị trí expected chunk.")
    lines.append("- [ ] Rà soát chiến lược chunking để giảm câu bị cắt mảnh.")
    lines.append("- [ ] Thêm dashboard theo dõi fail case theo nhóm lỗi sau mỗi lần benchmark.")
    lines.append("- [ ] Thiết lập gate phụ: block nếu số retrieval miss vượt ngưỡng.")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_summarize():
    benchmark_data = load_benchmark_results()
    summary = build_summary(benchmark_data)

    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    write_failure_analysis(benchmark_data, summary, path="analysis/failure_analysis.md")

    print("\n📊 --- SUMMARY ---")
    print(json.dumps(summary["metrics_v1"], ensure_ascii=False, indent=2))
    print(json.dumps(summary["metrics_v2"], ensure_ascii=False, indent=2))
    print("\nΔ:")
    print(json.dumps(summary["delta"], ensure_ascii=False, indent=2))
    print("\nGate conditions:")
    for name, ok in summary["release_decision"]["conditions"].items():
        print(f"- {name}: {'PASS' if ok else 'FAIL'}")
    print(f"\n✅ Decision: {summary['release_decision']['decision']}")
    print("Saved: reports/summary.json")
    print("Updated: analysis/failure_analysis.md")


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
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"⏱ Total time: {total_time:.2f}s")

    return results, metrics


async def main():
    parser = argparse.ArgumentParser(description="Benchmark orchestrator for V1/V2 retrieval agent")
    parser.add_argument("--mode", type=str, choices=["benchmark", "summarize"], default="benchmark")
    parser.add_argument("--version", type=str, choices=["v1", "v2"])
    parser.add_argument("--both", action="store_true")

    args = parser.parse_args()
    if args.mode == "summarize":
        run_summarize()
        return
    if args.mode != "benchmark":
        print("❌ Unsupported mode")
        return

    dataset = load_dataset()

    v1_results, v2_results = None, None
    v1_metrics, v2_metrics = None, None

    # 🔹 chạy 1 version
    if args.version:
        results, metrics = await run_version(dataset, args.version)

        os.makedirs("reports", exist_ok=True)

        with open(f"reports/benchmark_{args.version}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        with open(f"reports/benchmark_{args.version}_metrics.json", "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        return

    # 🔹 chạy cả 2
    if args.both:
        v1_results, v1_metrics = await run_version(dataset, "v1")
        v2_results, v2_metrics = await run_version(dataset, "v2")

    else:
        print("❌ Bạn phải chọn --version hoặc --both")
        return

    # 🔹 ghi file chuẩn
    os.makedirs("reports", exist_ok=True)

    final_output = {
        "metadata": {
            "total_cases": len(dataset),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": CONFIG,
        },
        "v1_metrics": v1_metrics,
        "v2_metrics": v2_metrics,
        "v1_results": v1_results,
        "v2_results": v2_results,
    }

    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("\n✅ Saved to reports/benchmark_results.json")


if __name__ == "__main__":
    asyncio.run(main())
