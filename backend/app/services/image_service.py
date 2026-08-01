from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_image(image:UploadFile)->str:
    extension = image.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"
    file_path = UPLOAD_DIR / filename

    with open(file_path,"wb") as buffer:
        buffer.write(image.file.read())
    return str(file_path)