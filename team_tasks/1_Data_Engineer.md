# Thành viên 1 - Data Engineer (Chunking + Golden Set)

## Mục tiêu
Tạo nền dữ liệu chuẩn cho benchmark retrieval: **50 chunk_id khác nhau** và **50 câu hỏi map đúng các chunk_id đó**.

## Thông số cố định (không đổi)
- `CHUNK_SIZE_TOKENS = 256`
- `CHUNK_OVERLAP_TOKENS = 32`
- `TOTAL_QUESTIONS = 50`
- `RANDOM_SEED = 20260421` (dùng cho sampling chunk để tái lập)

## File phụ trách
- `data/synthetic_gen.py` (viết lại theo logic chunk-aware)
- `data/chunks.jsonl` (mỗi dòng là 1 chunk)
- `data/golden_set.jsonl` (50 câu benchmark)

## Nhiệm vụ chính
1. Đọc toàn bộ `data/docs/*.txt`.
2. Chunk văn bản theo chiến lược cố định: `256 tokens/chunk`, `overlap 32 tokens`.
3. Sinh `chunk_id` duy nhất theo format gợi ý: `doc_<file>_c_<index>`.
4. Lưu `chunks.jsonl` gồm:
   - `chunk_id`, `doc_name`, `chunk_text`, `char_start`, `char_end`.
5. Chọn đúng 50 chunk_id khác nhau để tạo benchmark set.
6. Tạo `golden_set.jsonl`, mỗi record có:
   - `question`, `expected_answer`, `expected_chunk_id`, `source_doc`, `difficulty`.

## Quy tắc chất lượng
- Không để 2 câu dùng chung `expected_chunk_id`.
- Câu hỏi phải truy xuất được câu trả lời trực tiếp từ chunk mục tiêu.
- Phân bổ câu hỏi trên nhiều file docs, không tập trung 1 tài liệu.

## Checklist bàn giao
- [ ] `data/chunks.jsonl` tạo thành công, có `chunk_id` ổn định.
- [ ] `data/golden_set.jsonl` đúng 50 dòng, đủ 50 chunk_id khác nhau.
- [ ] Có script validate uniqueness của `expected_chunk_id`.

## Interface gửi cho team
- Đảm bảo schema `golden_set.jsonl` cố định để team Retrieval/Runner đọc thẳng.

---

## Cần sửa gì (cực cụ thể)
### File 1: `data/synthetic_gen.py`
- Bỏ logic sinh câu hỏi từ `enriched_text` hard-code.
- Thêm hàm mới:
  - `load_docs(doc_dir: str) -> list[dict]`
  - `chunk_document(text: str, doc_name: str, chunk_size: int, overlap: int) -> list[dict]`
  - `build_chunks_from_docs(...) -> list[dict]`
  - `generate_questions_from_chunks(chunks: list[dict], target_n: int = 50) -> list[dict]`
  - `validate_golden_set(records: list[dict]) -> dict`
- Đầu ra script phải ghi **2 file**:
  - `data/chunks.jsonl`
  - `data/golden_set.jsonl`

### File 2 (nếu chưa có): `data/validate_dataset.py`
- Tạo script kiểm tra:
  - đủ 50 dòng,
  - 50 `expected_chunk_id` là unique,
  - mỗi `expected_chunk_id` tồn tại trong `chunks.jsonl`.

---

## Flow chạy code từng bước + output mong đợi
### Bước 1: Sinh chunk từ docs
- Chạy:
  - `python data/synthetic_gen.py --mode chunk`
- Script phải:
  1. Đọc tất cả file trong `data/docs`.
  2. Chunk theo `size=256`, `overlap=32`.
  3. Sinh `chunk_id`.
  4. Ghi `data/chunks.jsonl`.
- Output console mong đợi:
  - số file docs đã đọc,
  - tổng số chunk tạo ra,
  - thống kê chunk theo từng file.
- Output file mong đợi:
  - `data/chunks.jsonl` (mỗi dòng JSON) gồm:
    - `chunk_id`
    - `doc_name`
    - `chunk_text`
    - `char_start`
    - `char_end`

### Bước 2: Sinh golden set 50 câu từ chunk
- Chạy:
  - `python data/synthetic_gen.py --mode golden --n 50`
- Script phải:
  1. Đọc `chunks.jsonl`.
  2. Chọn 50 chunk_id khác nhau.
  3. Sinh 50 câu hỏi bám trực tiếp nội dung chunk.
  4. Mỗi câu gắn đúng 1 `expected_chunk_id`.
  5. Ghi `data/golden_set.jsonl`.
- Output console mong đợi:
  - `Selected 50 unique chunks`
  - `Generated 50 questions`
  - `Saved to data/golden_set.jsonl`
- Output file mong đợi (mỗi dòng):
  - `question`
  - `expected_answer`
  - `expected_chunk_id`
  - `source_doc`
  - `difficulty`

### Bước 3: Validate dataset
- Chạy:
  - `python data/validate_dataset.py`
- Script phải check:
  1. Golden set đủ 50 dòng.
  2. Không trùng `expected_chunk_id`.
  3. Tất cả `expected_chunk_id` map ngược được vào `chunks.jsonl`.
- Output console mong đợi:
  - `PASS: total_records = 50`
  - `PASS: unique_expected_chunk_ids = 50`
  - `PASS: all expected_chunk_id exist in chunks`

---

## Tiêu chí hoàn thành (DoD cá nhân)
- Có `data/chunks.jsonl` đúng schema.
- Có `data/golden_set.jsonl` đúng 50 dòng, đúng 50 chunk unique.
- Script validate chạy PASS 100%.
- Bàn giao kèm mẫu 3 record để team khác kiểm tra schema ngay.
