# 🧑‍💻 Thành viên 3: Chuyên gia Đánh giá Trí tuệ (LLM Judge Engineer)

## 📌 Trạng thái hiện tại: ✅ HOÀN THÀNH 100%
Đã tích hợp cơ chế **Đa giám khảo (GPT + Gemini)** và tính năng **Swap Test** chống thiên vị.

## 📁 File phần quyền xử lý chính
- `engine/llm_judge.py`
- `engine/test_judge.py`

## 🛠️ Trình tự các bước thực hiện (Đã làm)
1. **Định nghĩa Rubrics:** Đã thiết lập thang điểm 1-5 cho Accuracy và Tone.
2. **Multi-Model Consensus:** Đã tích hợp gọi song song `gpt-4o-mini` và `gemini-1.5-flash`.
3. **Cơ chế Fallback:** Nếu Gemini lỗi, hệ thống tự động fallback sang GPT để đảm bảo pipeline không bị ngắt.
4. **Bias Detection:** Đã cài đặt hàm `check_position_bias` (Kỹ thuật Swap Test) để phát hiện sự ưu tiên vị trí.

## ✅ Checklist kiểm tra
- [x] Chạy lệnh `python engine/test_judge.py` thành công (cần có đủ 2 API Keys).
- [x] Tính toán được `agreement_rate` giữa 2 giám khảo AI.
- [x] Trả về kết quả JSON chuẩn chứa `reasoning` của từng giám khảo.
- [x] Đã xử lý prefix `models/` cho Gemini để tránh lỗi SDK.

## 💡 Lưu ý cho Team
Class `LLMJudge` của bạn là "trọng tài" cuối cùng. Kết quả trung bình giữa 2 giám khảo sẽ là điểm số chính thức dùng để so sánh giữa phiên bản V1 và V2.
