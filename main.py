import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import chat
from core.exceptions import UniAIException
from middleware import exception_handler

load_dotenv()

app = FastAPI(
    title="UniAI",
    description="Universal AI Backend Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(UniAIException, exception_handler)
app.add_exception_handler(Exception, exception_handler)

# Include routers
app.include_router(chat.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to UniAI"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)