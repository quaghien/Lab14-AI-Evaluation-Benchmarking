# 🧑‍💻 Thành viên 5: Chuyên viên DevOps & Phân tích chất lượng (Release Gate & RCA)

## 📌 Trạng thái hiện tại: 🏗️ ĐANG THỰC HIỆN (FINAL INTEGRATION)
Cần cập nhật `main.py` để sử dụng Runner thật và thực hiện phân tích kết quả sau cùng.

## 📁 File phần quyền xử lý chính
- `main.py`
- `analysis/failure_analysis.md`

## 🛠️ Nhiệm vụ cần làm ngay
1. **Cài đặt Entrypoint:** Chỉnh sửa `main.py` để khởi tạo `BenchmarkRunner` với `RetrievalEvaluator` và `LLMJudge` (không dùng mock class nữa).
2. **Xử lý kết quả Regression:** 
   - So sánh `avg_score`, `hit_rate` và `ndcg` giữa V1 và V2.
   - Nếu bất kỳ chỉ số nào giảm > 10%, phải in ra cảnh báo 🛑 **BLOCK RELEASE**.
3. **Báo cáo 5 Whys:** Sau khi có file `reports/benchmark_results.json`, hãy chọn ra 3 case tệ nhất để phân tích trong file `failure_analysis.md`.
4. **Check Lab:** Chạy `python check_lab.py` để đảm bảo định dạng bài nộp chuẩn 100%.

## ✅ Checklist kiểm tra
- [ ] File `reports/summary.json` chứa đầy đủ các chỉ số (Hit Rate, MRR, NDCG, Agreement Rate).
- [ ] Log console hiển thị rõ ràng quá trình so sánh V1 vs V2.
- [ ] Bài lab pass qua được script `check_lab.py`.

## 💡 Lưu ý cho Team
Bướcc cuối cùng này khẳng định giá trị của dự án. Hãy tập trung vào việc chứng minh: "Bản cải tiến V2 thực sự tốt hơn bản V1 về mặt con số cụ thể".
