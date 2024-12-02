from fastapi import FastAPI
from pydantic import BaseModel
from queue import Queue
from threading import Lock


app = FastAPI()


MESSAGE_QUEUE = Queue()
LOCK = Lock()


class EnqueueRequest(BaseModel):
    message: str

@app.post("/push")
async def enqueue(request: EnqueueRequest):
    """Add a message to the queue."""
    with LOCK:
        MESSAGE_QUEUE.put(request.message)
    return {"status": "success", "message": "Message enqueued"}

@app.get("/pop")
async def dequeue():
    """Remove and return a message from the queue."""
    with LOCK:
        if MESSAGE_QUEUE.empty():
            return {"status": "empty", "message": None}
        message = MESSAGE_QUEUE.get()
    return {"status": "success", "message": message}

@app.post("/flush")
async def flush():
    """Clear the queue."""
    with LOCK:
        while not MESSAGE_QUEUE.empty():
            MESSAGE_QUEUE.get()
    return {"status": "success", "message": "Queue flushed"}

@app.get("/status")
async def status():
    """Get the current queue status."""
    with LOCK:
        size = MESSAGE_QUEUE.qsize()
    return {"status": "success", "size": size}
