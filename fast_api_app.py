from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/ping")
async def delayed_response():
    await asyncio.sleep(2)  # Simulate a delay of 2 seconds
    return {"message": "This response was delayed by 2 seconds"}