from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
import os
from PIL import Image
import shutil

app = FastAPI()
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 5 * 1024 * 1024
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_and_optimize(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with Image.open(file_path) as img:
        img.convert("RGB").save(file_path, "JPEG", quality=85)

@app.post("/upload/")
async def upload(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks):
    for file in files:
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail=f"Файл {file.filename} недопустимого формату.")
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"Файл {file.filename} перевищує максимальний розмір.")
        background_tasks.add_task(save_and_optimize, file)
    return {"message": "Файли завантажені та обробляються."}