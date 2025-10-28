# main.py - FastAPI 入口
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import AnswerAgent
from app.feishu_api import FeishuSync
import os


app = FastAPI()
agent = AnswerAgent()
feishu = FeishuSync()


class QueryRequest(BaseModel):
 q: str


@app.post('/query')
async def query(req: QueryRequest):
 res = await agent.answer(req.q)
 return {'answer': res}


@app.post('/sync')
async def sync_docs():
# 手动触发同步
 await feishu.sync_all_docs()
 return {'status': 'ok'}


# 局部健康检查
@app.get('/health')
async def health():
  return {'status': 'ok'}


if __name__ == '__main__':
 import uvicorn
 uvicorn.run('app.main:app', host=os.getenv('BACKEND_HOST', '127.0.0.1'), port=int(os.getenv('BACKEND_PORT', 8000)), reload=True)