import asyncio
from typing import Dict

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent.retriever import Retriever

load_dotenv()

GENERATION_MODEL = "gpt-4o-mini"
TOP_K = 3

SYSTEM_PROMPT = (
    "Bạn là trợ lý hỗ trợ nội bộ. Trả lời câu hỏi dựa trên các đoạn tài liệu được cung cấp. "
    "Nếu tài liệu không đủ thông tin, hãy nói rõ điều đó."
)


class MainAgent:
    def __init__(self, version: str = "v2"):
        self.version = version
        self.name = f"SupportAgent-{version}"
        self.retriever = Retriever()
        self.client = AsyncOpenAI()

    async def query(self, question: str) -> Dict:
        retrieval_result = self.retriever.retrieve(question, version=self.version, top_k=TOP_K)

        context = "\n\n---\n\n".join(retrieval_result["retrieved_chunks"])
        user_message = f"Tài liệu tham khảo:\n{context}\n\nCâu hỏi: {question}"

        response = await self.client.chat.completions.create(
            model=GENERATION_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        return {
            "answer": answer,
            "retrieved_chunk_ids": retrieval_result["retrieved_chunk_ids"],
            "retrieved_chunks": retrieval_result["retrieved_chunks"],
            "retrieval_mode": retrieval_result["retrieval_mode"],
            "metadata": {
                "model": GENERATION_MODEL,
                "tokens_used": tokens_used,
            },
        }


if __name__ == "__main__":
    async def test():
        agent = MainAgent(version="v2")
        resp = await agent.query("Làm thế nào để đổi mật khẩu?")
        print(f"Answer: {resp['answer']}")
        print(f"Retrieved: {resp['retrieved_chunk_ids']}")
        print(f"Mode: {resp['retrieval_mode']}")
        print(f"Tokens: {resp['metadata']['tokens_used']}")

    asyncio.run(test())
