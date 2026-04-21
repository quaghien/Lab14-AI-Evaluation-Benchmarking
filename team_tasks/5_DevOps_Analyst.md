# Thành viên 5 - DevOps & Quality Analyst (Regression Gate)

## Mục tiêu
Tổng hợp benchmark V1/V2 thành báo cáo định lượng và ra quyết định release gate rõ ràng.

## Thông số cố định (không đổi)
- `GATE_MIN_DELTA_HIT_RATE = +0.10`
- `GATE_MIN_DELTA_MRR = +0.10`
- `GATE_MIN_DELTA_FINAL_SCORE = 0.00`
- `TOTAL_CASES = 50`

## File phụ trách
- `main.py`
- `analysis/failure_analysis.md`
- `check_lab.py` (nếu cần cập nhật rule check mới)

## Nhiệm vụ chính
1. Thiết kế `summary.json` có các nhóm:
   - `metrics_v1`,
   - `metrics_v2`,
   - `delta` (v2 - v1),
   - `release_decision`.
2. Định nghĩa gate rule tối thiểu:
   - `hit_rate_v2 >= hit_rate_v1`,
   - `mrr_v2 >= mrr_v1`,
   - không giảm `final_score` quá ngưỡng cho phép.
3. Xuất 2 file chuẩn:
   - `reports/benchmark_results.json`,
   - `reports/summary.json`.
4. Viết `analysis/failure_analysis.md`:
   - chọn 3-5 case fail điển hình,
   - phân tích 5 Whys tập trung vào retrieval mismatch (expected_chunk_id vs retrieved).

## Checklist bàn giao
- [ ] Console in rõ so sánh V1 vs V2.
- [ ] Có kết luận `APPROVE` hoặc `BLOCK RELEASE` dựa trên ngưỡng.
- [ ] `python check_lab.py` chạy pass trước khi nộp.

## Interface gửi cho team
- Quy định schema report cố định để các thành viên khác có thể đối chiếu nhanh.

---

## Cần sửa gì (cực cụ thể)
### File 1: `main.py`
- Sau khi có kết quả V1 và V2, thêm khối:
  - tính aggregate cho từng version,
  - tính delta,
  - áp dụng gate rule,
  - ghi `reports/summary.json`.

### File 2: `analysis/failure_analysis.md`
- Điền nội dung thật từ kết quả benchmark:
  - top case fail theo retrieval miss,
  - top case fail theo judge thấp.
- Viết 5 Whys tập trung nguyên nhân retrieval.

### File 3: `check_lab.py` (nếu cần)
- Mở rộng validate:
  - kiểm tra trong `summary.json` có đủ `metrics_v1`, `metrics_v2`, `delta`, `release_decision`.

---

## Flow chạy code từng bước + output mong đợi
### Bước 1: Tạo báo cáo tổng hợp từ raw benchmark
- Chạy:
  - `python main.py --mode summarize`
- Script phải:
  1. đọc `reports/benchmark_results.json`.
  2. tính metric trung bình cho v1/v2.
  3. tính delta v2-v1.
  4. quyết định release gate.
  5. ghi `reports/summary.json`.
- Output console mong đợi:
  - bảng metric v1, v2.
  - `delta_hit_rate`, `delta_mrr`, `delta_final_score`.
  - quyết định cuối cùng: `APPROVE` hoặc `BLOCK RELEASE`.

### Bước 2: Chạy rule gate
- Rule bắt buộc:
  - `hit_rate_v2 >= hit_rate_v1`
  - `mrr_v2 >= mrr_v1`
  - `delta_hit_rate >= +0.10`
  - `delta_mrr >= +0.10`
  - `delta_final_score >= 0.00`
- Output mong đợi:
  - in rõ condition nào pass/fail.
  - nếu fail condition nào thì block.

### Bước 3: Viết failure analysis từ dữ liệu thật
- Chạy:
  - đọc `reports/benchmark_results.json` và lọc case fail.
- Ghi vào `analysis/failure_analysis.md`:
  1. nhóm lỗi retrieval miss.
  2. nhóm lỗi hallucination.
  3. 3-5 case xấu nhất (5 Whys).
- Output mong đợi:
  - mỗi case có `expected_chunk_id` vs `retrieved_chunk_ids`.
  - có root cause + action item rõ.

### Bước 4: Validate trước khi nộp
- Chạy:
  - `python check_lab.py`
- Output mong đợi:
  - PASS tồn tại file bắt buộc.
  - PASS schema summary/report.
  - cảnh báo nếu thiếu trường quan trọng.

---

## Schema `summary.json` bắt buộc
- `metadata`: timestamp, total_cases.
- `metrics_v1`: hit_rate, mrr, avg_judge_score, avg_latency.
- `metrics_v2`: hit_rate, mrr, avg_judge_score, avg_latency.
- `delta`: delta_hit_rate, delta_mrr, delta_judge_score, delta_latency.
- `release_decision`: APPROVE/BLOCK + reasons.

---

## Tiêu chí hoàn thành (DoD cá nhân)
- Có `reports/summary.json` đúng schema trên.
- Có quyết định release dựa trên số liệu, không cảm tính.
- `failure_analysis.md` có bằng chứng từ case thật, không template rỗng.
