import asyncio
import time
from typing import List, Dict


class BenchmarkRunner:
    def __init__(self, agent, retrieval_evaluator, judge, config):
        self.agent = agent
        self.retrieval_evaluator = retrieval_evaluator
        self.judge = judge
        self.config = config

    async def run_single_test(self, test_case: Dict) -> Dict:
        start_time = time.perf_counter()

        try:
            question = test_case["question"]
            expected_chunk_id = test_case["expected_chunk_id"]
            expected_answer = test_case.get("expected_answer", "")

            # 🔹 1. Agent
            response = await self.agent.query(question)

            answer = response["answer"]
            retrieved_chunk_ids = response["retrieved_chunk_ids"]
            retrieved_chunks = response["retrieved_chunks"]

            # 🔹 2. Retrieval metrics
            retrieval_scores = self.retrieval_evaluator.evaluate_case(
                expected_chunk_id,
                retrieved_chunk_ids,
                top_k=self.config["TOP_K"]
            )

            # 🔹 3. Judge (CÓ context)
            judge_result = await self.judge.evaluate_multi_judge(
                question,
                answer,
                expected_answer,
                retrieved_chunks
            )

            final_score = judge_result["final_score"]
            agreement_rate = judge_result["agreement_rate"]

            # 🔹 4. Latency
            latency = time.perf_counter() - start_time

            # 🔹 5. Status
            status = (
                "pass"
                if final_score >= self.config["STATUS_PASS_THRESHOLD_FINAL_SCORE"]
                else "fail"
            )

            return {
                "question": question,
                "expected_chunk_id": expected_chunk_id,
                "retrieved_chunk_ids": retrieved_chunk_ids,
                "hit_rate": retrieval_scores["hit_rate"],
                "mrr": retrieval_scores["mrr"],
                "ndcg": retrieval_scores["ndcg"],
                "final_score": final_score,
                "agreement_rate": agreement_rate,
                "latency": latency,
                "status": status
            }

        except Exception as e:
            return {
                "question": test_case.get("question"),
                "status": "error",
                "error": str(e),
                "latency": time.perf_counter() - start_time
            }

    async def run_all(self, dataset: List[Dict], concurrency: int) -> List[Dict]:
        semaphore = asyncio.Semaphore(concurrency)
        total = len(dataset)

        async def run_with_limit(idx, case):
            async with semaphore:
                result = await self.run_single_test(case)
                print(f"processed {idx+1}/{total}")
                return result

        tasks = [
            run_with_limit(i, case)
            for i, case in enumerate(dataset)
        ]

        results = await asyncio.gather(*tasks)
        return results

    def aggregate_metrics(self, results: List[Dict]) -> Dict:
        valid = [r for r in results if r["status"] != "error"]

        if not valid:
            return {}

        avg_latency = sum(r["latency"] for r in valid) / len(valid)
        hit_rate = sum(r["hit_rate"] for r in valid) / len(valid)
        mrr = sum(r["mrr"] for r in valid) / len(valid)
        ndcg = sum(r["ndcg"] for r in valid) / len(valid)

        pass_rate = sum(1 for r in valid if r["status"] == "pass") / len(valid)

        return {
            "avg_latency": avg_latency,
            "hit_rate": hit_rate,
            "mrr": mrr,
            "ndcg": ndcg,
            "pass_rate": pass_rate,
            "total": len(results),
            "valid": len(valid)
        }