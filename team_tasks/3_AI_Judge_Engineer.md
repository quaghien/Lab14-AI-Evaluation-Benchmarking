# 🧑‍💻 Thành viên 3: Chuyên gia Đánh giá Trí tuệ (LLM Judge Engineer)

## 📌 Tổng quan mục tiêu
Xây dựng "Trọng tài AI" khách quan, chống thiên vị. Trọng tài này sẽ so sánh trực tiếp câu trả lời của Agent với Answer Key (Ground Truth) để chấm điểm (từ 1-5). Phải dùng ít nhất 2 model khác nhau làm trọng tài (Consensus Engine). Trị giá 20% tổng điểm dự án.

## 📁 File phần quyền xử lý chính
- `engine/llm_judge.py`

## 🛠️ Trình tự các bước cần làm
1. **Thiết kế Rubrics (Tiêu chí chấm):** Chỉnh sửa constructor `__init__` để thiết lập rõ tiêu chí (Accuracy: 1-5, Tone: 1-5).
2. **Tích hợp hai Model Judge:** Trong hàm `evaluate_multi_judge`, thực hiện việc gọi API tới 2 Model khác nhau (Ví dụ: `gpt-4o-mini` và `claude-3-haiku` hoặc `gemini-1.5-flash`).
   - Cung cấp cùng 1 Prompt chấm điểm: Bao gồm `question`, `answer` (của Agent), và `ground_truth` (Câu trả lời đúng).
   - Yêu cầu các LLM này trả về điểm (format JSON/Dict).
3. **Cơ chế đồng thuận (Consensus Logic):** Sau khi lấy được điểm của Model A và Model B:
   - Tính `final_score` (Trung bình cộng).
   - Tính `agreement_rate` (1.0 nếu đồng thuận tuyệt đối, 0.5 nếu lệch 1 điểm, hoặc có thể dùng công thức tuỳ biến). Trả về 0 nếu độ chênh lệch cực lớn (Ví dụ Model A cho 1, Model B cho 5).
4. **Nâng cao (Tuỳ chọn ăn điểm):** Implement hàm `check_position_bias` để chạy test hoán đổi vị trí câu trả lời xem model có ưu ái câu nào được đưa vào trước không.

## ✅ Tiêu chí hoàn thành (Checklist)
- [ ] Prompt được định nghĩa rõ ràng với thang điểm cụ thể (Rubrics).
- [ ] Code gọi được ít nhất 2 model LLM có chức năng Judge.
- [ ] Tính trung bình điểm chính xác (`final_score`).
- [ ] Xây dựng rule độ tin cậy giữa hai model (`agreement_rate`).
- [ ] Output trả về Dictionary đúng định dạng đầu ra mong muốn.

## 💡 Nơi nhận kết quả
Mã nguồn hàm đánh giá `MultiModelJudge` của bạn sẽ được gọi thông qua vòng chạy cho mỗi test case bên trong `engine/runner.py`. Bạn hoàn toàn có thể tự truyền chuỗi string tự chế để test Judge model có chấm sát điểm không.
