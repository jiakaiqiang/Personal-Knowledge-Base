# scheduler.py - 定时同步示例（APScheduler）
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.feishu_api import FeishuSync


scheduler = AsyncIOScheduler()
feishu = FeishuSync()


def start_scheduler():
    scheduler.add_job(lambda: feishu.sync_all_docs(), 'interval', minutes=30)
    scheduler.start()


# 在 uvicorn 启动后导入并调用 start_scheduler()