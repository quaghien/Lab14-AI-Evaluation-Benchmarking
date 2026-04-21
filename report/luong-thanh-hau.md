# Bao cao ca nhan - luong-thanh-hau (Data Engineer)

## Vai tro va pham vi
- Vai tro: Data Engineer (chunking + golden set).
- File phu trach: `data/synthetic_gen.py`, `data/validate_dataset.py`.
- Dau ra ban giao: `data/chunks.jsonl`, `data/golden_set.jsonl`.

## Cong viec da thuc hien
1. Xay dung lai script sinh du lieu theo huong chunk-aware:
   - `load_docs(doc_dir: str) -> list[dict]`
   - `chunk_document(text: str, doc_name: str, chunk_size: int, overlap: int) -> list[dict]`
   - `build_chunks_from_docs(...) -> list[dict]`
   - `generate_questions_from_chunks(chunks: list[dict], target_n: int = 50) -> list[dict]`
   - `validate_golden_set(records: list[dict]) -> dict`

2. Hoan thien flow chay theo dung quy dinh team:
   - `python data/synthetic_gen.py --mode chunk`
   - `python data/synthetic_gen.py --mode golden --n 50`
   - `python data/validate_dataset.py`

3. Tao script kiem tra doc lap:
   - Kiem tra du 50 records.
   - Kiem tra 50 `expected_chunk_id` unique.
   - Kiem tra tat ca `expected_chunk_id` ton tai trong `chunks.jsonl`.

## Ket qua dau ra (thuc te)
- So file docs doc vao: `5`
- Tong so chunk tao ra: `51`
- Phan bo chunk:
  - `access_control_sop`: 11
  - `sla_p1_2026`: 11
  - `hr_leave_policy`: 10
  - `it_helpdesk_faq`: 10
  - `policy_refund_v4`: 9
- Golden set:
  - Tong records: `50`
  - Unique `expected_chunk_id`: `50`
  - Duplicate `expected_chunk_id`: `0`
  - Missing fields: `0`

## Ket qua validate
- `PASS: total_records = 50`
- `PASS: unique_expected_chunk_ids = 50`
- `PASS: all expected_chunk_id exist in chunks`

## Mau 3 records de team check schema nhanh
```json
{"question":"Theo tai lieu sla_p1_2026, quy dinh nao mo ta noi dung: 'Sau khi khắc phục, viết incident report trong vòng 24 giờ'?","expected_answer":"Sau khi khắc phục, viết incident report trong vòng 24 giờ.","expected_chunk_id":"doc_sla_p1_2026_c_8","source_doc":"sla_p1_2026","difficulty":"easy"}
{"question":"Theo tai lieu hr_leave_policy, quy dinh nao mo ta noi dung: 'Nhân viên gửi yêu cầu nghỉ phép qua hệ thống HR Portal (https://hr.com'?","expected_answer":"Nhân viên gửi yêu cầu nghỉ phép qua hệ thống HR Portal (https://hr.company.internal) ít nhất 3 ngày làm việc trước ngày nghỉ.","expected_chunk_id":"doc_hr_leave_policy_c_4","source_doc":"hr_leave_policy","difficulty":"medium"}
{"question":"Theo tai lieu it_helpdesk_faq, quy dinh nao mo ta noi dung: 'Nhắc nhở sẽ được gửi 30 ngày trước khi hết hạn'?","expected_answer":"Nhắc nhở sẽ được gửi 30 ngày trước khi hết hạn.","expected_chunk_id":"doc_it_helpdesk_faq_c_6","source_doc":"it_helpdesk_faq","difficulty":"easy"}
```

## Ghi chu ban giao
- Schema `golden_set.jsonl` da co dinh gom 5 truong:
  `question`, `expected_answer`, `expected_chunk_id`, `source_doc`, `difficulty`.
- Dataset da san sang de team Retrieval/Runner su dung truc tiep.
