# 🧑‍💻 Thành viên 2: Kỹ sư Đánh giá Tìm kiếm (Retrieval Evaluator)

## 📌 Trạng thái hiện tại: ✅ HOÀN THÀNH 100%
Code đã được nâng cấp thêm chỉ số **NDCG** và hỗ trợ tham số `top_k` linh hoạt.

## 📁 File phần quyền xử lý chính
- `engine/retrieval_eval.py`

## 🛠️ Trình tự các bước thực hiện (Đã làm)
1. **Hit Rate & MRR:** Đã cài đặt logic tính toán chuẩn.
2. **Bổ sung NDCG:** Đã thêm hàm tính `calculate_ndcg` để đánh giá chất lượng xếp hạng tài liệu (Expert level).
3. **Tham số linh hoạt:** Hàm `evaluate_batch` đã nhận tham số `top_k` (mặc định là 3).
4. **Unit Test:** Đã viết bộ test cực kỳ chi tiết trong block `if __name__ == "__main__":`.

## ✅ Checklist kiểm tra
- [x] Chạy lệnh `python engine/retrieval_eval.py` đạt kết quả `All tests passed!`.
- [x] Hỗ trợ đủ 3 chỉ số: Hit Rate, MRR, NDCG.
- [x] Logic xử lý được nhiều kiểu tên Key khác nhau từ dữ liệu đầu vào.
- [x] Code đã được tối ưu hóa theo chuẩn Google Style.

## 💡 Lưu ý cho Team
Class `RetrievalEvaluator` của bạn sẽ được Thành viên số 4 (Runner) gọi ra để chấm điểm cho từng đợt truy xuất của Agent.
