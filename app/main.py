from fastapi import FastAPI
from app.api.endpoints import queue

app = FastAPI(title="Appointo Queue System")

app.include_router(queue.router, prefix="/queue", tags=["Queue"])
