# 🧑‍💻 Thành viên 4: Kiến trúc sư Tối ưu hóa (Async Runner)

## 📌 Tổng quan mục tiêu
Tạo ra một cỗ máy (Engine) cực khỏe có thể chạy bài test Evaluation siêu tốc cho 50+ cases trong thời gian < 2 phút thông qua Async. Đảm bảo tránh sập hệ thống (Rate limit) khi gọi LLM liên tục. Trị giá 15% tổng điểm.

## 📁 File phần quyền xử lý chính
- `engine/runner.py`
- `agent/main_agent.py` (Chỉnh sửa mock hoặc dùng thật)

## 🛠️ Trình tự các bước cần làm
1. **Kiểm tra chuẩn hoá Input/Output:** Đảm bảo `MainAgent` trong `agent/main_agent.py` (khi chạy) trả về đúng keys cần thiết cho Evaluator (`answer`, chuỗi `contexts`, mảng `retrieved_ids`).
2. **Quản lý Batches trong `run_all`:** Hiện tại hàm `run_all` có `batch_size = 5`. Chỉnh sửa và test kỹ lại cách chạy ngầm các coroutines bằng `asyncio.gather(*tasks)`.
3. **Xử lý Rate Limit Retry:** Thêm block Try/Catch trong vòng lặp Async phòng trường hợp một số API (LLM Judge) bị time out hoặc báo lỗi vì Rate Limit. Nếu rớt thì thực hiện backoff/thử lại.
4. **Tích hợp các Class từ đội khác:** Ở hàm `run_single_test`, bạn sẽ sử dụng `ExpertEvaluator` (từ Member 2) và `MultiModelJudge` (từ Member 3). Hãy lấy output dictionary mà họ trả về, gói nó vào trong Dict lớn `{"ragas": ..., "judge": ...}`.

## ✅ Tiêu chí hoàn thành (Checklist)
- [ ] `MainAgent` đã sẵn sàng và input đồng nhất khớp với test cases (JsonL).
- [ ] Hoàn tất code async trong `runner.py` với asyncio.
- [ ] Có thiết lập ngắt nghỉ batch phù hợp (Ví dụ: Chạy lượt 10 requests, nghỉ 1s rồi chạy tiếp 10 req tiếp theo).
- [ ] Cấu trúc kết quả Dict từ hàm `run_all` trả về mảng kết quả của 50 test cases.
- [ ] (Tuỳ chọn) Lưu log thời gian xử lý tổng hợp để in ra "Tổng thời gian Benchmark".

## 💡 Nơi nhận kết quả
Mã nguồn hàm `BenchmarkRunner` của bạn sẽ được gọi trực tiếp bằng entrypoint ở `main.py` bởi Kỹ sư DevOps (Thành viên 5). Bạn có thể viết thêm logic giả lập độ trễ trong Agent để chạy test tốc độ Async trước khi ráp code với mọi người!
