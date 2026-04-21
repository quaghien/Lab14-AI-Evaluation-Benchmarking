# Báo cáo Cá nhân - Thành viên 4: Async Runner

- **Họ và tên:** Nguyễn Thị Thu Hiền
- **MSSV:** 2A202600212
- **Vai trò:** Lead Optimizer (Async Execution & Integration)

---

## 🛠️ Đóng góp kỹ thuật (Engineering Contribution)
- Thiết kế và hoàn thiện `engine/runner.py` theo hướng async: triển khai `run_single_test`, `run_all`, `aggregate_metrics` để chạy benchmark ổn định trên toàn bộ dataset.
- Tích hợp `asyncio.Semaphore` để giới hạn concurrency, giảm rủi ro rate limit khi gọi nhiều request đồng thời tới retrieval/generation/judge.
- Bổ sung cơ chế xử lý lỗi theo từng case (`status=error`) để pipeline không crash toàn batch khi một test thất bại.
- Chuẩn hóa output per-case phục vụ phân tích downstream: `question`, `expected_chunk_id`, `retrieved_chunk_ids`, `hit_rate`, `mrr`, `final_score`, `agreement_rate`, `latency`, `status`.

---

## 🧠 Chiều sâu chuyên môn (Technical Depth)
- Em sử dụng **Semaphore** thay vì chạy gather toàn bộ để giữ throughput ổn định và tránh vượt ngưỡng request/token theo phút của provider.
- Chiến lược chạy async giúp giảm đáng kể thời gian xử lý so với tuần tự, đồng thời vẫn kiểm soát được tài nguyên bằng tham số `CONCURRENCY`.
- Việc tách rõ phần đo `latency` theo từng case và aggregate theo version giúp team đánh đổi được giữa chất lượng (hit rate, mrr, final_score) và hiệu năng vận hành.

---

## 🚀 Giải quyết vấn đề (Problem Solving)
- Khi interface giữa các module chưa đồng nhất (ví dụ khác tên trường retrieval/judge), em ưu tiên chuẩn hóa schema ở runner để hạn chế if/else phân tán trong nhiều file.
- Khi gặp lỗi API hoặc thiếu trường output ở một số case, em xử lý theo hướng fail-safe: lưu lỗi theo case, tiếp tục batch, và để analyst vẫn có dữ liệu tổng hợp.
- Em phối hợp với các thành viên khác để giữ contract đầu ra ổn định, giúp `main.py` có thể ghi report benchmark nhất quán cho cả V1/V2.

---

## ✍️ Tự đánh giá (Self-Reflection)
- Qua bài lab này, em học rõ rằng vai trò “ráp nối” không chỉ là nối hàm chạy được, mà phải đảm bảo tính ổn định, khả năng quan sát (observability) và tính tương thích giữa các module.
- Khó khăn nhất là xử lý sai lệch schema và lỗi runtime khi nhiều thành phần phát triển song song.
- Em thấy giá trị lớn nhất của Async Runner là biến các module rời rạc thành một pipeline benchmark thực chiến, có thể dùng để ra quyết định kỹ thuật dựa trên số liệu.
