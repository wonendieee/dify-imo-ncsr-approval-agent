from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Excel Download Service")


@app.post("/upload")
async def upload(file: UploadFile = File(...), desired_name: str | None = Form(default=None)):
    # Respect the uploaded filename when available; allow desired_name override from extra form data.
    final_name = desired_name or file.filename or f"{uuid4().hex}.xlsx"
    # avoid path traversal
    final_name = final_name.replace("/", "_").replace("\\", "_")
    target = STORAGE_DIR / final_name
    content = await file.read()
    target.write_bytes(content)
    return {
        "download_url": f"http://127.0.0.1:8000/files/{final_name}",
        "file_name": final_name,
    }


@app.get("/files/{filename}")
def download(filename: str):
    safe_name = filename.replace("/", "_").replace("\\", "_")
    target = STORAGE_DIR / safe_name
    return FileResponse(target, filename=safe_name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
