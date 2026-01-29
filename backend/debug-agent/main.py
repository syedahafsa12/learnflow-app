from fastapi import FastAPI
from pydantic import BaseModel
import logging

app = FastAPI(title="debug-agent", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "debug-agent"}

@app.get("/")
async def root():
    return {"message": "Welcome to debug-agent"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
