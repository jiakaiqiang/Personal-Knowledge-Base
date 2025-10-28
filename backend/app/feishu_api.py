# feishu_api.py - 简化示例：获取飞书文档 plain text
import os
import httpx
from dotenv import load_dotenv
load_dotenv()


FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET')
TOKEN_URL = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
DOC_TEXT_API = 'https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/plain_text'


class FeishuSync:
    def __init__(self):
        self._token = None


async def _get_tenant_token(self):
    if self._token:
        return self._token
    async with httpx.AsyncClient() as client:
        resp = await client.post(TOKEN_URL, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET})
        data = resp.json()
        self._token = data.get('tenant_access_token')
        return self._token


async def fetch_doc_text(self, document_id: str) -> str:
    token = await self._get_tenant_token()
    url = DOC_TEXT_API.format(document_id=document_id)
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data.get('data', {}).get('content', '')


async def sync_all_docs(self):
# TODO: 在生产中你会先调用飞书 Drive API 列出文档，然后遍历。
# 这里示例：从环境变量读取要同步的 doc id 列表。
    doc_ids = os.getenv('FEISHU_DOC_IDS', '')
    if not doc_ids:
         return
    for doc_id in doc_ids.split(','):
        txt = await self.fetch_doc_text(doc_id.strip())
        # 将文本切分并存入向量库
        from app.embedding import chunk_and_embed
        await chunk_and_embed(doc_id, txt)