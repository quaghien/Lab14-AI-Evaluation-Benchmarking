# Thành viên 3 - LLM Judge Engineer

## Mục tiêu
Đánh giá chất lượng câu trả lời cho cùng bộ retrieval output của V1/V2, đồng thời giữ pipeline judge ổn định để so sánh công bằng.

## Thông số cố định (không đổi)
- `GPT_MODEL = gpt-4o-mini`
- `GEMINI_MODEL = gemini-1.5-flash`
- `SCORE_RANGE = 1..5`
- `WEIGHT_ACCURACY = 0.7`
- `WEIGHT_GROUNDING = 0.3`
- `AGREEMENT_STRICT_DIFF = 1` (chênh > 1 là bất đồng)
- `REQUEST_TIMEOUT_SECONDS = 30`

## File phụ trách
- `engine/llm_judge.py`
- `engine/test_judge.py`

## Nhiệm vụ chính
1. Chuẩn hóa rubric judge theo 2 tiêu chí:
   - `accuracy` (so với `expected_answer`),
   - `grounding` (có bám context retrieval hay bịa).
2. Giữ multi-judge (GPT + Gemini) và trả về:
   - `final_score`,
   - `agreement_rate`,
   - `reasoning`.
3. Thiết kế prompt judge để input gồm:
   - `question`,
   - `agent_answer`,
   - `expected_answer`,
   - `retrieved_chunks` (để chấm grounding).
4. Thêm cơ chế fail-safe:
   - 1 model lỗi vẫn trả được kết quả tối thiểu để runner không dừng.

## Quy tắc benchmark
- Judge không được biết đó là V1 hay V2 (blind evaluation).
- Dùng cùng 1 rubric cho cả 2 version.
- Log raw judgment để phục vụ failure analysis.

## Checklist bàn giao
- [ ] Chạy `python engine/test_judge.py` pass.
- [ ] Output JSON luôn đúng schema dù có lỗi API tạm thời.
- [ ] Có test case cho câu đúng, câu sai, câu hallucination.

## Interface gửi cho team
- Hàm `evaluate_multi_judge(...)` trả về format ổn định để `runner.py` tổng hợp.

---

## Cần sửa gì (cực cụ thể)
### File 1: `engine/llm_judge.py`
- Cập nhật prompt để judge nhận đủ input:
  - `question`
  - `agent_answer`
  - `expected_answer`
  - `retrieved_chunks`
- Chuẩn hóa rubric thành 2 trục:
  - `accuracy_score` (1-5)
  - `grounding_score` (1-5)
- Tính:
  - `final_score` (weighted avg)
  - `agreement_rate`
- Thêm fallback:
  - nếu 1 model lỗi -> dùng model còn lại + flag `degraded_mode=true`.

### File 2: `engine/test_judge.py`
- Viết test cho 4 nhóm case:
  1. answer đúng + context đúng.
  2. answer đúng một phần.
  3. answer sai/hallucination.
  4. retrieval sai context nhưng answer cố “đoán”.

---

## Flow chạy code từng bước + output mong đợi
### Bước 1: Kiểm tra biến môi trường
- Kiểm tra `.env` có:
  - `OPENAI_API_KEY`
  - `GEMINI_API_KEY`
- Output mong đợi:
  - nếu thiếu key -> báo lỗi rõ model nào thiếu.

### Bước 2: Chạy smoke test judge
- Chạy:
  - `python engine/test_judge.py --mode smoke`
- Output console mong đợi:
  - in `final_score`, `agreement_rate`, `degraded_mode`.
  - không crash dù 1 provider timeout.

### Bước 3: Chạy test đầy đủ 4 case
- Chạy:
  - `python engine/test_judge.py --mode full`
- Output mong đợi:
  - Case đúng: điểm cao (>=4).
  - Case hallucination: điểm thấp (<=2.5).
  - Case retrieval lệch: grounding thấp.
  - Case partial: điểm trung bình.

### Bước 4: Verify schema output cho Runner
- Mỗi lần gọi `evaluate_multi_judge(...)` phải trả JSON có:
  - `final_score`
  - `agreement_rate`
  - `accuracy_score_avg`
  - `grounding_score_avg`
  - `individual_judgments`
  - `degraded_mode`
- Output mong đợi:
  - runner parse được mà không cần if/else thêm.

---

## Tiêu chí hoàn thành (DoD cá nhân)
- Judge chạy ổn định cho batch 50 case.
- Không có response rỗng hoặc JSON malformed.
- Có log reasoning đủ dùng để viết failure analysis.
