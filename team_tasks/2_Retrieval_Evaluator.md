# 🧑‍💻 Thành viên 2: Kỹ sư Đánh giá Tìm kiếm (Retrieval Evaluator)

## 📌 Tổng quan mục tiêu
Xây dựng module đánh giá chất lượng của VectorDB. Chức năng này phải trả lời được câu hỏi: Khi người dùng hỏi, hệ thống RAG có lôi ra được đúng mảnh tài liệu gốc không? (Trị giá 15% tổng điểm dự án).

## 📁 File phần quyền xử lý chính
- `engine/retrieval_eval.py`

## 🛠️ Trình tự các bước cần làm
1. **Cài đặt logic Hit Rate:** Hoàn thiện hàm `calculate_hit_rate(expected_ids, retrieved_ids, top_k)`.
   - **Định nghĩa:** Nếu mảng `retrieved_ids` lấy được bất kỳ một ID nào nằm trong `expected_ids` -> Hit = 1. Ngược lại = 0.
2. **Cài đặt logic MRR:** Hoàn thiện hàm `calculate_mrr(expected_ids, retrieved_ids)`.
   - **Định nghĩa:** Lấy vị trí index đầu tiên (1-based) mà tài liệu đúng xuất hiện trong `retrieved_ids`. `MRR = 1 / index`. Nếu không xuất hiện -> MRR = 0.
3. **Tổng hợp dữ liệu (Batch Eval):** Hoàn thiện hàm `evaluate_batch(dataset)`.
   - Lặp qua tất cả dữ liệu (dict chứa câu hỏi và ids) và gọi 2 hàm trên để trả về `avg_hit_rate` và `avg_mrr` cho toàn bộ bộ dữ liệu.

## ✅ Tiêu chí hoàn thành (Checklist)
- [ ] Code xong logic `calculate_hit_rate`.
- [ ] Code xong logic `calculate_mrr` (Chú ý tránh lỗi chia cho 0).
- [ ] Hàm `evaluate_batch` trả về được Dictionary chứa kết quả trung bình hợp lệ: `{"avg_hit_rate": x, "avg_mrr": y}`.
- [ ] Có tự viết vài hàm Test nhỏ với các mảng Arrays tuỳ ý để xác nhận công thức toán học chạy đúng. 

## 💡 Nơi nhận kết quả
Kết quả của bạn (Class `RetrievalEvaluator`) sẽ được tích hợp trực tiếp vào trong `engine/runner.py` bởi Kỹ sư Async. Bạn có thể tự chủ động tạo list mảng mock data để test mà không cần chờ Agent hay Runner hoàn chỉnh!
