# 🚀 Phân công nhiệm vụ Lab 14: AI Evaluation Factory

Chào nhóm, dựa trên yêu cầu từ `README.md` và tiêu chí chấm điểm `GRADING_RUBRIC.md`, dự án này được chia thành 5 module độc lập. Mọi người có thể code song song, tự test bằng dữ liệu giả (mock data) mà không cần chờ người khác làm xong.

---

## 🧑‍💻 Thành viên 1: Chuyên gia Dữ liệu (Synthetic Data Generation)
**Mục tiêu:** Tạo ra "Golden Dataset" chuẩn để kiểm thử hệ thống.
- **File phụ trách:** `data/synthetic_gen.py`
- **Nhiệm vụ chính:** 
  1. Viết prompt để gọi LLM sinh ra ít nhất **50 test cases**.
  2. Mỗi test case phải bao gồm: `question`, `expected_answer`, `context` và `expected_ids` (hoặc `ground_truth_ids`).
  3. Cần đảm bảo có các bộ "Red Teaming" (câu hỏi lừa) để test độ hóc búa.
  4. Lưu xuất data ra file `data/golden_set.jsonl`.
- **Cách làm độc lập:** Bạn chỉ cần quan tâm tới việc dùng API (OpenAI/Anthropic...) để sinh data text. Không cần tương tác với bất kỳ file nào khác ngoài `synthetic_gen.py`.

---

## 🧑‍💻 Thành viên 2: Kỹ sư Đánh giá Tìm kiếm (Retrieval Evaluator)
**Mục tiêu:** Đảm bảo hệ thống chấm điểm VectorDB hoạt động chuẩn xác (chiếm 15% tổng điểm).
- **File phụ trách:** `engine/retrieval_eval.py`
- **Nhiệm vụ chính:** 
  1. Code logic toán học cho hàm `calculate_hit_rate` (Kiểm tra ID đúng có lọt top K không).
  2. Code logic tính `calculate_mrr` (Mean Reciprocal Rank - thứ hạng của ID đúng trong top K).
  3. Trả về kết quả trung bình cho toàn bộ bộ dữ liệu truyền vào hàm `evaluate_batch`.
- **Cách làm độc lập:** Đây hoàn toàn là logic thuật toán. Hãy tự tạo các mảng mock test chứa list arrays IDs và ID đáp án để kiểm tra kết quả tính toán có ra đúng công thức hay không, không cần phải chạy Agent để test.

---

## 🧑‍💻 Thành viên 3: Chuyên gia Đánh giá Trí tuệ (Multi-Judge Consensus)
**Mục tiêu:** Xây dựng Giám khảo AI công tâm, dùng nhiều model để chống thiên vị (chiếm 20% tổng điểm).
- **File phụ trách:** `engine/llm_judge.py`
- **Nhiệm vụ chính:** 
  1. Viết prompt chấm điểm cụ thể cho AI Judge dựa trên `accuracy` và `tone`.
  2. Tích hợp ít nhất 2 LLM model khác nhau (ví dụ: GPT-4o và Claude 3.5, hoặc Gemini) để cùng chấm điểm 1 cặp (câu trả lời của Agent vs. Ground Truth).
  3. Xây dựng logic tính trung bình điểm `final_score` và tỷ lệ đồng thuận `agreement_rate` (nếu hai model lệch nhau > 1 điểm thì tính là bất đồng).
- **Cách làm độc lập:** Hãy gọi trực tiếp hàm `evaluate_multi_judge` với các chuỗi ký tự ảo làm input, kiểm tra xem nó gọi API và xử lý JSON trả ra chuẩn không.

---

## 🧑‍💻 Thành viên 4: Kiến trúc sư Tối ưu hóa (Async Metrics & Runner)
**Mục tiêu:** Hệ thống phải chạy cực nhanh (chấm 50 cases dưới 2 phút) và ổn định (chiếm 15% tổng điểm).
- **File phụ trách:** `engine/runner.py` và `agent/main_agent.py`
- **Nhiệm vụ chính:** 
  1. Hoàn thiện hàm `run_all` dùng `asyncio.gather()` để chạy đồng thời các test case. 
  2. Cài đặt giới hạn `batch_size` (semaphore) hợp lý để tránh lỗi Rate Limit khi gọi API quá nhanh.
  3. Đảm bảo format đầu ra của `MainAgent.query()` khớp hoàn toàn với pipeline ở Runner.
- **Cách làm độc lập:** Tự gán các hàm giả lập sleep (`await asyncio.sleep()`) vào hàm `evaluate` và `judge` trong runner. Viết một hàm test chạy 50 dummy cases xem tổng thời gian và tốc độ xử lý batch có đúng ý đồ logic asyncio không.

---

## 🧑‍💻 Thành viên 5: Chuyên viên DevOps & Phân tích chất lượng (Release Gate & RCA)
**Mục tiêu:** Kiểm soát tự động Regression và phân tích chuyên sâu lỗi (chiếm 25% tổng điểm).
- **File phụ trách:** `main.py` và `analysis/failure_analysis.md`
- **Nhiệm vụ chính:**
  1. Trong `main.py`: Viết logic quyết định tự động **Tự Release** (nếu Delta > 0) hoặc **Rollback/Từ chối** (nếu Delta <= 0) bằng cách so sánh điểm của V1 và V2. Xuất được các file json yêu cầu.
  2. Trong báo cáo: Đi sâu vào kết quả output JSON sau cùng, áp dụng kỹ thuật "5 Whys" để chỉ ra được nguyên nhân gốc vì sao AI trả lời sai (do chunking, retrieval hay LLM hallucination).
  3. Check script cuối cùng: Chạy `check_lab.py` để đảm bảo bài nộp không thiếu file.
- **Cách làm độc lập:** Viết sẵn khung báo cáo `failure_analysis.md`. Test logic trong `main.py` bằng cách tự gán kết quả dict ảo cho `v1_summary` và `v2_summary`.

---

## 🤝 Quy trình rắp ráp cuối cùng (Trong 30 phút cuối):
- Mọi người push file nhánh của mình vào nhánh `main`.
- Chạy `python data/synthetic_gen.py` thật để tạo file `golden_set`.
- Chạy `python main.py` chạy toàn bộ pipeline async.
- Nhóm 5 lấy các file JSON sinh ra chạy để lấy evidence điền báo cáo Markdown.
- Chạy `python check_lab.py` -> Nộp bài!
