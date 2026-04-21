# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 50
- **V1:** hit_rate=0.48, mrr=0.42, avg_judge_score=2.90
- **V2:** hit_rate=0.88, mrr=0.76, avg_judge_score=4.19
- **Release decision:** APPROVE

## 2. Phân nhóm lỗi (Failure Clustering)
| Nhóm lỗi | Số lượng | Mô tả |
|---|---:|---|
| Retrieval miss | 6 | expected_chunk_id không nằm trong retrieved_chunk_ids |
| Low judge score | 10 | final_score < 3.0 |
| Hallucination-like | 7 | Retrieval hit nhưng điểm judge vẫn thấp |

## 3. 5 Whys cho các case tệ nhất

### Case #1
- **Question:** Theo tài liệu hr_leave_policy, quy định nào mô tả nội dung: "Tối đa 5 ngày phép năm chưa dùng được chuyển sang năm tiếp theo."?
- **Expected chunk:** `doc_hr_leave_policy_c_1`
- **Retrieved chunks:** `['doc_hr_leave_policy_c_0', 'doc_hr_leave_policy_c_2', 'doc_hr_leave_policy_c_7']`
- **Scores:** hit_rate=0.00, mrr=0.00, final_score=1.00
1. **Why 1:** Vì expected chunk không xuất hiện trong top-k.
2. **Why 2:** Vì truy vấn và chunk có độ tương đồng ngữ nghĩa chưa đủ cao.
3. **Why 3:** Vì chunking cố định làm phân mảnh thông tin quan trọng.
4. **Why 4:** Vì chưa có bước reranking để sửa thứ tự kết quả gần đúng.
5. **Why 5:** Vì chưa có cảnh báo tự động khi retrieval miss tăng đột biến.
6. **Root Cause:** Retrieval quality chưa ổn định ở các câu mô tả quy định dài.

### Case #2
- **Question:** Theo tài liệu it_helpdesk_faq, quy định nào mô tả nội dung: "Nếu vẫn không có, tạo ticket P2 kèm địa chỉ email gửi và thời gian gửi."?
- **Expected chunk:** `doc_it_helpdesk_faq_c_8`
- **Retrieved chunks:** `['doc_it_helpdesk_faq_c_7', 'doc_it_helpdesk_faq_c_9', 'doc_sla_p1_2026_c_7']`
- **Scores:** hit_rate=0.00, mrr=0.00, final_score=1.00
1. **Why 1:** Vì expected chunk không xuất hiện trong top-k.
2. **Why 2:** Vì truy vấn và chunk có độ tương đồng ngữ nghĩa chưa đủ cao.
3. **Why 3:** Vì chunking cố định làm phân mảnh thông tin quan trọng.
4. **Why 4:** Vì chưa có bước reranking để sửa thứ tự kết quả gần đúng.
5. **Why 5:** Vì chưa có cảnh báo tự động khi retrieval miss tăng đột biến.
6. **Root Cause:** Retrieval quality chưa ổn định ở các câu mô tả quy định dài.

### Case #3
- **Question:** Theo tài liệu sla_p1_2026, quy định nào mô tả nội dung: "v2025.1 (2025-03-01): Phiên bản đầu tiên."?
- **Expected chunk:** `doc_sla_p1_2026_c_10`
- **Retrieved chunks:** `['doc_sla_p1_2026_c_10', 'doc_hr_leave_policy_c_0', 'doc_policy_refund_v4_c_1']`
- **Scores:** hit_rate=1.00, mrr=1.00, final_score=1.00
1. **Why 1:** Vì expected chunk đã có nhưng điểm judge vẫn thấp.
2. **Why 2:** Vì câu trả lời generation chưa trích đúng ý trong chunk.
3. **Why 3:** Vì prompt trả lời chưa ép bám sát expected answer đủ mạnh.
4. **Why 4:** Vì chưa có hậu kiểm nội dung trước khi trả lời cuối.
5. **Why 5:** Vì chưa có test hồi quy theo nhóm câu dễ nhầm lẫn ngữ nghĩa gần.
6. **Root Cause:** Generation/prompting chưa ổn định dù retrieval đã hit.

### Case #4
- **Question:** Theo tài liệu sla_p1_2026, quy định nào mô tả nội dung: "Tự động escalate sau 90 phút không có phản hồi."?
- **Expected chunk:** `doc_sla_p1_2026_c_5`
- **Retrieved chunks:** `['doc_sla_p1_2026_c_5', 'doc_sla_p1_2026_c_3', 'doc_sla_p1_2026_c_4']`
- **Scores:** hit_rate=1.00, mrr=1.00, final_score=1.00
1. **Why 1:** Vì expected chunk đã có nhưng điểm judge vẫn thấp.
2. **Why 2:** Vì câu trả lời generation chưa trích đúng ý trong chunk.
3. **Why 3:** Vì prompt trả lời chưa ép bám sát expected answer đủ mạnh.
4. **Why 4:** Vì chưa có hậu kiểm nội dung trước khi trả lời cuối.
5. **Why 5:** Vì chưa có test hồi quy theo nhóm câu dễ nhầm lẫn ngữ nghĩa gần.
6. **Root Cause:** Generation/prompting chưa ổn định dù retrieval đã hit.

### Case #5
- **Question:** Theo tài liệu hr_leave_policy, quy định nào mô tả nội dung: "Thứ 2 - Thứ 6, 8:30 - 17:30."?
- **Expected chunk:** `doc_hr_leave_policy_c_9`
- **Retrieved chunks:** `['doc_hr_leave_policy_c_9', 'doc_hr_leave_policy_c_0', 'doc_policy_refund_v4_c_8']`
- **Scores:** hit_rate=1.00, mrr=1.00, final_score=1.30
1. **Why 1:** Vì expected chunk đã có nhưng điểm judge vẫn thấp.
2. **Why 2:** Vì câu trả lời generation chưa trích đúng ý trong chunk.
3. **Why 3:** Vì prompt trả lời chưa ép bám sát expected answer đủ mạnh.
4. **Why 4:** Vì chưa có hậu kiểm nội dung trước khi trả lời cuối.
5. **Why 5:** Vì chưa có test hồi quy theo nhóm câu dễ nhầm lẫn ngữ nghĩa gần.
6. **Root Cause:** Generation/prompting chưa ổn định dù retrieval đã hit.

## 4. Kế hoạch cải tiến (Action Plan)
- [ ] Thêm reranker sau FAISS để cải thiện vị trí expected chunk.
- [ ] Rà soát chiến lược chunking để giảm câu bị cắt mảnh.
- [ ] Thêm dashboard theo dõi fail case theo nhóm lỗi sau mỗi lần benchmark.
- [ ] Thiết lập gate phụ: block nếu số retrieval miss vượt ngưỡng.
