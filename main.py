import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from database import Database
from app.route import NoteBotRoute


class MaxSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int = 5 * 1024 * 1024):  # Default: 5 MB
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.max_upload_size:
            raise HTTPException(status_code=413, detail="Payload Too Large")
        return await call_next(request)


# Initialize FastAPI application
app = FastAPI(
    title="NoteBot API",
    description="API for transcription and note-taking services.",
    version="1.0.0"
)

# Initialize Database
Database()

# Add Middleware
app.add_middleware(MaxSizeLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NoteBot Routes
notebot_router = NoteBotRoute(None, None)  # Replace `None` with actual dependencies if required
app.include_router(notebot_router.router, prefix="/api/notebot")


# Static files or additional endpoints
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_HTML = os.path.join(BASE_DIR, "website/index.html")
PRIVACY_HTML = os.path.join(BASE_DIR, "website/privacy_policy.html")



# Main entry point for running the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
