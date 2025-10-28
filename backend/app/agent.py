import os
from openai import OpenAI
from app.embedding import embed_texts
from app.vector_store import VectorStore
from dotenv import load_dotenv
load_dotenv()


LLM = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
CHAT_MODEL = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini')
EMBED_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-large')


class AnswerAgent:
    def __init__(self):
      self.vs = VectorStore()


async def answer(self, query: str):
# 1. embed query
    q_emb = (await embed_texts([query]))[0]
    # 2. retrieve
    docs = self.vs.query(q_emb, top_k=5)
    context = "\n---\n".join([d['text'] for d in docs])
    # 3. call LLM
    prompt = f"你是一个基于飞书文档构建的知识库助手。根据下面内容回答用户问题，若内容不足请说明并给出合理建议。\n\n上下文：\n{context}\n\n问题：{query}\n\n答案："
    resp = LLM.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
        {"role":"system","content":"你是知识库助手。回答要简洁并引用来源 chunk_id。"},
        {"role":"user","content":prompt}
        ],
        max_tokens=800
    )
    # 解析并返回
    ans = resp.choices[0].message.content
    return ans