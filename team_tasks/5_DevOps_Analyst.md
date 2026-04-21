# 🧑‍💻 Thành viên 5: Chuyên viên DevOps & Phân tích chất lượng (Release Gate & RCA)

## 📌 Tổng quan mục tiêu
Tạo "Chốt chặn phát hành" (Release Gate) hoàn toàn tự động, phân xử cho quá trình nâng cấp Agent V1 -> V2. Ghi chép dữ liệu output ra file JSON đầy đủ cho hệ thống chấm điểm và thực hiện phân tích 5 Whys. Trị giá 25% tổng điểm!

## 📁 File phần quyền xử lý chính
- `main.py`
- Báo cáo phân tích: `analysis/failure_analysis.md`

## 🛠️ Trình tự các bước cần làm
1. **Delta/Regression Gate (`main.py`):** 
   - Đảm bảo logic tính toán chênh lệch (Delta) điểm số giữa model cũ (`Agent_V1`) và model mới (`Agent_V2_Optimized`).
   - Viết tính năng đọc dict JSON từ Async Runner (Thành viên 4), tính trung bình lại (nếu chưa có) và ghi vào 2 file JSON được yêu cầu: `reports/summary.json` và `reports/benchmark_results.json`.
   - Cài rule Gate: Chỉ nếu Delta >= Y và `agreement_rate` > Z thì mới in ra console ACCEPT RELEASE.
2. **Khảo sát hệ thống thực tế (Root Cause Analysis):** 
   - Sau khi Runner sinh ra file `reports/benchmark_results.json`, hãy mở file này ra, đọc các test cases bị đánh giá Fail hoặc có điểm thấp (< 3).
   - Mở file Markdown `analysis/failure_analysis.md` và viết bản điều tra "5-Whys". Hỏi liên tục 5 lần "Vì sao" để tìm ra lỗi là rớt ở bước Chunking, Nhầm Prompt, Model Ảo giác hay Retrieval quá tệ?  
3. **Thẩm định bài nộp (Format Verification):** 
   - Chạy lệnh `python check_lab.py` để script check pass 100%. Script này quét sự tồn tại và cấu trúc file JSON bạn vừa lưu ở `reports`.

## ✅ Tiêu chí hoàn thành (Checklist)
- [ ] Chạy thành công quy trình so sánh "V1 Base vs V2 Optimized" trong `main.py`.
- [ ] Hệ thống tự động đẩy kết quả JSON ra thư mục `reports/`.
- [ ] File json xuất ra có đủ nội dung `metrics:{ hit_rate, agreement_rate, avg_score}`.
- [ ] Bạn đã điền hoàn tất tài liệu phân tích 5-whys vào folder `analysis/`.
- [ ] Script kiểm tra `python check_lab.py` chạy KHÔNG còn báo lỗi đỏ nào!

## 💡 Nơi nhận kết quả
Mọi con mắt đổ dồn vào bước này. Đây là thao tác cuối của vòng lặp Lab 14. Bạn cần chờ file JSON từ Team Data, nhận bộ Code Async từ M2, M3, M4 để hoàn thành cái chạy cuối cùng này! Rất quan trọng!
