import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analyze, analyze_excel, auth, chat, deduplicate, download, excel_dedup, history, similarity, upload

app = FastAPI(title="Semantic Validator API")

# Allow the configured origin AND any localhost port (handles Vite auto-incrementing)
_LOCALHOST_RE = re.compile(r"^http://localhost:\d+$")


def _is_allowed_origin(origin: str) -> bool:
    return origin == settings.CORS_ORIGIN or bool(_LOCALHOST_RE.match(origin))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # broad allow — fine for local dev
    allow_credentials=False,      # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analyze.router)
app.include_router(upload.router)
app.include_router(deduplicate.router)
app.include_router(download.router)
app.include_router(analyze_excel.router)
app.include_router(chat.router)
app.include_router(history.router)
app.include_router(similarity.router)
app.include_router(excel_dedup.router)
