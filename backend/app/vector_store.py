# vector_store.py - 使用 Chroma 本地存储
import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
load_dotenv()


PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', './chroma_persist')


class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(persist_directory=PERSIST_DIR))
        self.collection = self.client.get_or_create_collection(name='feishu_docs')


def add(self, embedding, metadata):
# embedding: list[float]
# metadata: dict
    self.collection.add(
    documents=[metadata['text']],
    metadatas=[metadata],
    ids=[metadata['chunk_id']],
    embeddings=[embedding]
    )


def query(self, embedding, top_k=5):
    results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
    # 返回文档文本和 metadata
    out = []
    for ids, docs, metadatas, distances in zip(results['ids'], results['documents'], results['metadatas'], results['distances']):
        for _id, doc, meta, dist in zip(ids, docs, metadatas, distances):
            out.append({'id': _id, 'text': doc, 'meta': meta, 'score': dist})
    return out