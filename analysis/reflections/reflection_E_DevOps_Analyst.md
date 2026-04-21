# Báo cáo Cá nhân - Thành viên 5: DevOps Analyst

- **Họ và tên:** Hồ Quang Hiển
- **MSSV:** 2A202600059
- **Vai trò:** DevOps & Quality Analyst (Release Gate & RCA)

---

## 🛠️ Đóng góp kỹ thuật (Engineering Contribution)
- Hoàn thiện chế độ `--mode summarize` trong `main.py`: đọc `reports/benchmark_results.json`, tính metric V1/V2, tính delta và áp dụng release gate tự động.
- Chuẩn hóa đầu ra `reports/summary.json` theo nhóm trường `metadata`, `metrics_v1`, `metrics_v2`, `delta`, `release_decision` để phục vụ chấm tự động và regression review.
- Cập nhật `analysis/failure_analysis.md` từ dữ liệu benchmark thật (không dùng template rỗng), gồm failure clustering và 5 Whys cho các case fail điển hình.
- Nâng cấp `check_lab.py` để kiểm tra schema summary mới, kiểm tra đủ các trường bắt buộc và in cảnh báo nếu thiếu metric quan trọng.

---

## 🧠 Chiều sâu chuyên môn (Technical Depth)
- **Release Gate** được xây theo nguyên tắc “không release theo cảm tính”: chỉ APPROVE khi các điều kiện định lượng cùng pass (`delta_hit_rate >= 0.10`, `delta_mrr >= 0.10`, `delta_judge_score >= 0.00`, đồng thời V2 không kém V1 ở hit_rate/mrr).
- Cách làm này giúp chặn regression âm dù điểm tổng có thể nhìn “ổn”, vì gate kiểm từng thành phần chất lượng retrieval và answer quality.
- **5 Whys** được dùng để truy gốc nguyên nhân theo chuỗi từ triệu chứng bề mặt (điểm thấp/miss retrieval) tới nguyên nhân hệ thống (chunking, thứ tự retrieval, thiếu reranker, thiếu guardrail kiểm thử).

---

## 🚀 Giải quyết vấn đề (Problem Solving)
- Khi pipeline đã có `benchmark_results.json` nhưng chưa có `summary.json`, mình thêm luồng summarize độc lập để không phải chạy lại benchmark nặng mỗi lần cần quyết định release.
- Khi phát hiện lỗi đọc file do chạy lệnh song song (summary chưa ghi xong đã check), mình chuyển sang chạy tuần tự để đảm bảo tính nhất quán trước khi check_lab.
- Với JSON output không đồng nhất giữa các module, mình chuẩn hóa schema và viết kiểm tra đầu vào/đầu ra rõ ràng để tránh lỗi silent fail ở bước tổng hợp.

---

## ✍️ Tự đánh giá (Self-Reflection)
- Qua bài lab này, mình học được rằng phần “hậu kiểm” (evaluation, gate, RCA) quan trọng không kém phần xây agent; nếu không có gate định lượng, hệ thống rất dễ release bản kém chất lượng.
- Mình thấy kỹ năng quan trọng nhất của vai trò DevOps/Analyst là biến dữ liệu benchmark thành quyết định kỹ thuật có thể giải trình được.
- Theo mình, guardrails tối thiểu cho hệ thống AI thực tế gồm: regression gate theo ngưỡng cố định, logging đầy đủ theo case, fallback khi model/provider lỗi, kiểm soát chi phí-token, và quy trình RCA bắt buộc sau mỗi vòng benchmark lớn.
