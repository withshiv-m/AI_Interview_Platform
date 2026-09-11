from pathlib import Path
import re
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_ROOT = BASE_DIR / "uploads"
RESUME_DIR = UPLOAD_ROOT / "resumes"
JOB_DIR = UPLOAD_ROOT / "jobs"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def ensure_upload_dirs():
    RESUME_DIR.mkdir(parents=True, exist_ok=True)
    JOB_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    name = Path(filename or "upload").name
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[:180] or "upload"


def build_resume_path(filename: str) -> Path:
    safe = sanitize_filename(filename)
    return RESUME_DIR / f"{uuid.uuid4().hex}_{safe}"
