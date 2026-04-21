# Thành viên 4 - Async Runner & Benchmark Executor

## Mục tiêu
Lắp ráp pipeline chạy benchmark đồng thời cho 50 câu, trả kết quả chi tiết cho **cả V1 và V2** trên cùng dataset.

## Thông số cố định (không đổi)
- `TOTAL_CASES = 50`
- `CONCURRENCY = 8`
- `TOP_K = 3`
- `MAX_RETRY_PER_CASE = 1`
- `STATUS_PASS_THRESHOLD_FINAL_SCORE = 3.0`

## File phụ trách
- `engine/runner.py`
- `main.py` (phần orchestration gọi runner)

## Nhiệm vụ chính
1. Viết `run_single_test(case, version)`:
   - gọi retrieval theo version (V1 hoặc V2),
   - gọi generation trả lời dựa trên context retrieval,
   - chấm retrieval metrics và judge metrics.
2. Viết `run_all(dataset, version)` dùng async + semaphore.
3. Viết hàm chạy 2 lượt benchmark:
   - lượt 1: V1 trên 50 câu,
   - lượt 2: V2 trên 50 câu.
4. Gom kết quả theo format:
   - per-case result,
   - aggregate metrics theo version.

## Yêu cầu hiệu năng
- Dùng `asyncio.gather` + `asyncio.Semaphore` để tránh rate limit.
- Log thời gian chạy tổng và latency trung bình/case.

## Checklist bàn giao
- [ ] Pipeline không crash khi một case lỗi (đánh dấu `status=error` và chạy tiếp).
- [ ] Kết quả có đầy đủ retrieval + judge + latency.
- [ ] Có thể xuất ra `reports/benchmark_results.json`.

## Interface gửi cho team
- Trả về object rõ 2 nhánh `v1` và `v2` để Analyst tính delta.

---

## Cần sửa gì (cực cụ thể)
### File 1: `engine/runner.py`
- Viết/chuẩn hóa các hàm:
  - `run_single_test(case: dict, version: str) -> dict`
  - `run_all(dataset: list[dict], version: str, concurrency: int) -> list[dict]`
  - `aggregate_metrics(results: list[dict]) -> dict`
- Trong `run_single_test` bắt buộc có các bước:
  1. gọi agent retrieval + answer.
  2. chấm retrieval metric từ `expected_chunk_id`.
  3. chấm judge metric.
  4. đo latency.
  5. bắt exception để không làm gãy batch.

### File 2: `main.py` (phần orchestrate)
- Thêm luồng chạy tuần tự:
  - chạy `run_all(..., version="v1")`
  - chạy `run_all(..., version="v2")`
- Ghi raw result ra `reports/benchmark_results.json`.

---

## Flow chạy code từng bước + output mong đợi
### Bước 1: Chạy benchmark V1
- Chạy:
  - `python main.py --mode benchmark --version v1`
- Hành vi mong đợi:
  1. đọc `data/golden_set.jsonl`.
  2. chạy 50 case bằng async + `Semaphore(8)`.
  3. lưu kết quả nhánh V1.
- Output console mong đợi:
  - progress: `processed 10/50 ... 50/50`
  - `avg_latency_v1`
  - `hit_rate_v1`, `mrr_v1`.

### Bước 2: Chạy benchmark V2
- Chạy:
  - `python main.py --mode benchmark --version v2`
- Output console mong đợi:
  - progress tương tự V1.
  - `avg_latency_v2`
  - `hit_rate_v2`, `mrr_v2`.

### Bước 3: Chạy full 2 version một lần
- Chạy:
  - `python main.py --mode benchmark --both`
- Hành vi mong đợi:
  1. chạy xong V1.
  2. chạy xong V2.
  3. ghi file raw result.
- Output file mong đợi:
  - `reports/benchmark_results.json`:
    - `v1_results`: list 50 case
    - `v2_results`: list 50 case

### Bước 4: Verify kết quả từng case
- Mỗi case output phải có:
  - `question`
  - `expected_chunk_id`
  - `retrieved_chunk_ids`
  - `hit_rate`
  - `mrr`
  - `final_score`
  - `agreement_rate`
  - `latency`
  - `status` (`pass`/`fail`/`error`)

---

## Gợi ý debug nhanh nếu lỗi
- Nếu nhiều `status=error`:
  - giảm `concurrency`.
- Nếu timeout judge:
  - bật fallback judge.
- Nếu thiếu `retrieved_chunk_ids`:
  - kiểm tra interface agent trả về.

---

## Tiêu chí hoàn thành (DoD cá nhân)
- Chạy full 50 case cho từng version không crash pipeline.
- File `benchmark_results.json` có đủ 2 nhánh v1/v2.
- Mỗi case có đủ trường để analyst tính delta.
