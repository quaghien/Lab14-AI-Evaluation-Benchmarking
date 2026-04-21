# 🧑‍💻 Thành viên 4: Kiến trúc sư Tối ưu hóa (Async Runner)

## 📌 Trạng thái hiện tại: 🏗️ ĐANG THỰC HIỆN (RE-CONFIG REQUIRED)
Cần cập nhật Runner để gọi vào các module "xịn" mà Thành viên 2 và 3 vừa hoàn thành.

## 📁 File phần quyền xử lý chính
- `engine/runner.py`

## 🛠️ Nhiệm vụ cần làm ngay
1. **Import Module thực:** Thay thế các placeholder bằng:
   ```python
   from engine.retrieval_eval import RetrievalEvaluator
   from engine.llm_judge import LLMJudge
   ```
2. **Tích hợp logic chấm điểm:** 
   - Trong `run_single_test`, hãy gọi `self.evaluator.calculate_hit_rate`, `calculate_mrr`, và `calculate_ndcg`.
   - Gọi `self.judge.evaluate_multi_judge` để lấy điểm đồng thuận.
3. **Cải tiến Async:** Sử dụng `asyncio.Semaphore` để giới hạn số lượng request đồng thời (Ví dụ: 10 requests cùng lúc) để tránh `RateLimitError` từ OpenAI/Gemini.

## ✅ Checklist kiểm tra
- [ ] Hàm `run_all` chạy mượt mà với 50 cases của Team Data.
- [ ] Kết quả trả về chứa đủ: `hit_rate`, `mrr`, `ndcg`, `final_score`, `agreement_rate`.
- [ ] Thời gian chạy toàn bộ 50 cases < 2 phút.

## 💡 Lưu ý cho Team
Bạn là người "lắp ráp" các module lại với nhau. Hãy đảm bảo dữ liệu truyền từ Agent sang Evaluator và Judge phải đúng schema (đúng tên Key).
