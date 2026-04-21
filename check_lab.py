import json
import os

def validate_lab():
    print("🔍 Đang kiểm tra định dạng bài nộp...")

    required_files = [
        "reports/summary.json",
        "reports/benchmark_results.json",
        "analysis/failure_analysis.md"
    ]

    # 1. Kiểm tra sự tồn tại của tất cả file
    missing = []
    for f in required_files:
        if os.path.exists(f):
            print(f"✅ Tìm thấy: {f}")
        else:
            print(f"❌ Thiếu file: {f}")
            missing.append(f)

    if missing:
        print(f"\n❌ Thiếu {len(missing)} file. Hãy bổ sung trước khi nộp bài.")
        return

    # 2. Kiểm tra nội dung summary.json
    try:
        with open("reports/summary.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ File reports/summary.json không phải JSON hợp lệ: {e}")
        return

    required_summary_keys = {"metadata", "metrics_v1", "metrics_v2", "delta", "release_decision"}
    if not required_summary_keys.issubset(set(data.keys())):
        print("❌ File summary.json thiếu một trong các trường bắt buộc: metadata, metrics_v1, metrics_v2, delta, release_decision.")
        return

    metrics_v1 = data["metrics_v1"]
    metrics_v2 = data["metrics_v2"]
    delta = data["delta"]
    release = data["release_decision"]

    print(f"\n--- Thống kê nhanh ---")
    print(f"Tổng số cases: {data['metadata'].get('total_cases', 'N/A')}")
    print(f"V1 avg_judge_score: {metrics_v1.get('avg_judge_score', 0):.2f}")
    print(f"V2 avg_judge_score: {metrics_v2.get('avg_judge_score', 0):.2f}")

    # EXPERT CHECKS
    has_retrieval = ("hit_rate" in metrics_v1) and ("hit_rate" in metrics_v2)
    if has_retrieval:
        print(
            "✅ Đã tìm thấy Retrieval Metrics "
            f"(V1: {metrics_v1['hit_rate']*100:.1f}% | V2: {metrics_v2['hit_rate']*100:.1f}%)"
        )
    else:
        print("⚠️ CẢNH BÁO: Thiếu Retrieval Metrics (hit_rate).")

    has_multi_judge = ("avg_judge_score" in metrics_v1) and ("avg_judge_score" in metrics_v2)
    if has_multi_judge:
        print("✅ Đã tìm thấy Multi-Judge Metrics (avg_judge_score ở cả V1/V2).")
    else:
        print("⚠️ CẢNH BÁO: Thiếu Multi-Judge Metrics (avg_judge_score).")

    has_delta = {"delta_hit_rate", "delta_mrr", "delta_judge_score", "delta_latency"}.issubset(set(delta.keys()))
    if has_delta:
        print("✅ Đã tìm thấy Delta metrics.")
    else:
        print("⚠️ CẢNH BÁO: Thiếu một số trường delta.")

    if isinstance(release, dict) and "decision" in release:
        print(f"✅ Release decision: {release['decision']}")
    else:
        print("⚠️ CẢNH BÁO: Thiếu release_decision.decision.")

    print("\n🚀 Bài lab đã sẵn sàng để chấm điểm!")

if __name__ == "__main__":
    validate_lab()
