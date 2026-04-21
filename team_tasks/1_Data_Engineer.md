# 🧑‍💻 Thành viên 1: Chuyên gia Dữ liệu (Synthetic Data Generation)

## 📌 Trạng thái hiện tại: ✅ HOÀN THÀNH 100%
Code đã được nâng cấp với cơ chế **Batching (10 câu/đợt)** và **Retry Logic** để đảm bảo không bị lỗi JSON hoặc Rate Limit.

## 📁 File phần quyền xử lý chính
- `data/synthetic_gen.py`
- `data/golden_set.jsonl` (Kết quả đầu ra)

## 🛠️ Trình tự các bước thực hiện (Đã làm)
1. **Thiết kế Prompt đa dạng:** Đã thêm các `diversity_hints` để AI không sinh trùng lặp câu hỏi.
2. **Cơ chế Retry:** Đã thêm Exponential Backoff để chống lỗi API.
3. **Red Teaming:** Đã tích hợp các câu hỏi "ảo giác" (hallucination) vào bộ dữ liệu.
4. **Đã sinh dữ liệu:** Đã tạo thành công 50 QA pairs chất lượng cao trong file `golden_set.jsonl`.

## ✅ Checklist kiểm tra
- [x] Chạy lệnh `python data/synthetic_gen.py` không lỗi.
- [x] Sinh ra file `data/golden_set.jsonl` đủ 50 dòng.
- [x] Các câu hỏi mang tính chuyên môn cao (bao gồm Hit Rate, MRR, NDCG).
- [x] Đã có file `.env.example` để hướng dẫn cấu hình API Key.

## 💡 Lưu ý cho Team
Bộ dữ liệu này là "xương sống" cho toàn bộ quá trình Benchmark phía sau. Các thành viên số 4 và 5 sẽ dùng file `golden_set.jsonl` này làm đầu vào.
