# embedding.py - 切分与索引
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
EMBED_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-large')


# 文本切分函数（非常简单）
def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


async def embed_texts(texts: list):
# 批量请求 embeddings
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    embeddings = [d.embedding for d in resp.data]
    return embeddings


    async def chunk_and_embed(doc_id: str, text: str):
        from app.vector_store import VectorStore
        vs = VectorStore()
        chunks = chunk_text(text)
        embeddings = await embed_texts(chunks)
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                meta = {"doc_id": doc_id, "chunk_id": f"{doc_id}::{i}", "text": chunk}
                vs.add(emb, meta)