# Báo cáo Cá nhân - Thành viên 2: Retrieval Evaluator

- **Họ và tên:** Tạ Thị Thùy Dương
- **MSSV:** 2A202600287
- **Vai trò:** Retrieval Engineer (FAISS Index & Search Metrics)

---

## 🛠️ Đóng góp kỹ thuật (Engineering Contribution)
*Mô tả các hàm bạn đã cài đặt trong `agent/retriever.py` và `agent/main_agent.py`.*

- **File chính đã triển khai/chỉnh sửa:** `agent/retriever.py` (mới hoàn toàn), `agent/main_agent.py` (thay thế mock).
- **Xây dựng FAISS Index từ tập chunks:**
  - `build_or_load_index()`: kiểm tra cache (`data/faiss.index` + `data/chunk_meta.json`); nếu đã tồn tại thì load ngay, tránh gọi API embedding lại.
  - `_build_index()`: đọc 51 chunks từ `data/chunks.jsonl`, embed theo batch 100 bằng `text-embedding-3-small`, normalize L2, build `IndexFlatIP`, lưu file index và metadata.
- **Implement 2 phiên bản retrieval để benchmark:**
  - `retrieve_v2()`: embed query → normalize → FAISS similarity search → trả `retrieved_chunk_ids`, `retrieved_chunks`, `scores`, `retrieval_mode="v2_faiss"`.
  - `retrieve_v1()`: dùng instance `random.Random(20260421)` riêng biệt; xác suất 50% đi nhánh random sample toàn bộ chunk meta, 50% đi nhánh FAISS; log `branch=random` hoặc `branch=faiss`; luôn trả `retrieval_mode="v1_random_mix"`.
  - `retrieve()`: wrapper nhận `version` parameter để chọn v1 hoặc v2.
- **CLI kiểm tra độc lập:**
  - `--build-index`: build và lưu index.
  - `--test-retrieve --version v1/v2 --trials N`: test retrieval đơn lẻ hoặc chạy N lần để xác nhận tỷ lệ random ~50%.
- **Cập nhật `agent/main_agent.py`:**
  - Nhận `version` parameter (`"v1"` hoặc `"v2"`), khởi tạo `Retriever`.
  - `query()` async: gọi retriever lấy context → gọi `gpt-4o-mini` sinh answer → trả schema chuẩn gồm `answer`, `retrieved_chunk_ids`, `retrieved_chunks`, `retrieval_mode`, `metadata`.
- **Kết quả kiểm tra sau khi hoàn thành:**
  - Build index: 51 chunks, embeddings shape (51, 1536), sinh đủ `data/faiss.index` + `data/chunk_meta.json`.
  - V2: top-3 chunk đúng ngữ nghĩa, scores ổn định khi lặp lại cùng query.
  - V1 trials=100: `branch=random` = 45/100 (45%) — nằm trong range 45–55% theo yêu cầu.

---

## 🧠 Chiều sâu chuyên môn (Technical Depth)
*Giải thích ý nghĩa và công thức của các chỉ số: **Hit Rate**, **MRR** (Mean Reciprocal Rank), và **NDCG** (Normalized Discounted Cumulative Gain).*

- **Hit Rate@K**: Metric nhị phân — bằng 1.0 nếu `expected_chunk_id` xuất hiện trong top-K kết quả retrieve, bằng 0.0 nếu không. Đơn giản nhưng không phân biệt được "tìm thấy ở vị trí 1" hay "tìm thấy ở vị trí K". Với V1 random, Hit Rate lý thuyết ≈ `top_k / total_chunks` = 3/51 ≈ 5.9%; V2 FAISS kỳ vọng cao hơn nhiều.

- **MRR (Mean Reciprocal Rank)**: MRR = 1 / rank_đầu_tiên_đúng. Rank 1 → 1.0, rank 2 → 0.5, rank 3 → 0.33, miss → 0. Khác với Hit Rate, MRR thưởng cho hệ thống đưa chunk đúng lên đầu danh sách — phản ánh trải nghiệm thực tế khi người dùng thường chỉ đọc kết quả đầu.

- **NDCG@K**: Normalized Discounted Cumulative Gain. DCG = Σ(rel_i / log₂(i+2)) với i là vị trí 0-indexed; rel_i = 1 nếu chunk đúng, 0 nếu không. IDCG là DCG lý tưởng (tất cả hit xếp ở đầu). NDCG = DCG / IDCG ∈ [0, 1]. Phạt mạnh hơn MRR khi có nhiều chunk liên quan bị xếp xuống thấp — metric phù hợp đánh giá ranking toàn diện.

---

## 🚀 Giải quyết vấn đề (Problem Solving)
*Mô tả cách bạn xử lý các trường hợp biên như mảng trống, không có kết quả tìm kiếm, hoặc sai lệch tên Key dữ liệu.*

- **Random state không tái lập khi dùng `random.seed()` global:**
  - Vấn đề: gọi `random.seed()` toàn cục ảnh hưởng đến các module khác đang dùng `random`, khiến benchmark không tái lập nếu thứ tự gọi thay đổi.
  - Giải pháp: dùng instance `random.Random(RANDOM_SEED)` riêng biệt gắn vào `self._rng` — chỉ ảnh hưởng nội bộ `Retriever`, không leak ra ngoài.

- **Tốn API embedding mỗi lần khởi động:**
  - Vấn đề: 51 chunks × embedding call = chi phí và thời gian lãng phí nếu index chưa thay đổi.
  - Giải pháp: `build_or_load_index()` kiểm tra sự tồn tại của `faiss.index` và `chunk_meta.json` trước — chỉ build khi thực sự cần thiết.

- **`IndexFlatIP` yêu cầu normalize L2 để tính cosine similarity đúng:**
  - Vấn đề: `IndexFlatIP` tính inner product thuần; nếu vector không được normalize thì score phụ thuộc vào độ lớn vector, không phản ánh góc cosine.
  - Giải pháp: gọi `faiss.normalize_L2()` cho toàn bộ embedding matrix lúc build index, và cho query vector trước mỗi lần search — đảm bảo inner product = cosine similarity.

- **FAISS trả index=-1 khi không đủ kết quả:**
  - Xử lý: bỏ qua các entry có `idx == -1` trong vòng lặp kết quả để tránh `IndexError` khi corpus nhỏ hơn `top_k`.

---

## ✍️ Tự đánh giá (Self-Reflection)
*Bạn học được gì qua bài lab này? Tại sao việc đánh giá Retrieval lại quan trọng đối với một hệ thống RAG chuyên nghiệp?*

- Qua bài lab này, tôi hiểu được tại sao Retrieval là tầng quyết định chất lượng của cả hệ thống RAG: dù LLM có mạnh đến đâu, nếu context đưa vào sai thì câu trả lời chắc chắn sai — "garbage in, garbage out".
- Việc tách V1 (random mix) và V2 (FAISS thuần) không chỉ là bài tập kỹ thuật mà là cách chứng minh bằng con số rằng hệ thống V2 thực sự tốt hơn — benchmark phải đo được, không chỉ "cảm giác đúng".
- Tôi hiểu sâu hơn về tầm quan trọng của reproducibility trong benchmark: cùng seed, cùng model, cùng data → cùng kết quả mọi lần chạy. Đây là điều kiện tối thiểu để so sánh có ý nghĩa giữa các phiên bản.
- Điều tôi tâm đắc nhất là cơ chế cache index (`build_or_load_index`): một quyết định nhỏ về engineering nhưng giảm đáng kể chi phí API và thời gian khởi động khi chạy benchmark nhiều lần.
- Nếu làm lại, tôi sẽ bổ sung thêm lệnh `--eval-golden` trong CLI để chạy nhanh Hit Rate và MRR trực tiếp trên toàn bộ 50 golden cases — giúp thấy ngay chênh lệch V1 vs V2 mà không cần đợi pipeline đầy đủ.
