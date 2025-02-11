import aiofiles
import re

from pathlib import Path
from fastapi import UploadFile
from fastapi.exceptions import HTTPException

from ..config import settings


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    sanitized = sanitized.replace(" ", "_")
    return sanitized

def get_default_upload_directory(file: UploadFile, base_path: str) -> str:
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        file_type_dir = "images"
    elif file_extension in ['txt', 'csv', 'json']:
        file_type_dir = "text_files"
    elif file_extension in ['pdf']:
        file_type_dir = "documents"
    else:
        file_type_dir = "others"
    
    upload_path = Path(base_path) / file_type_dir
    
    upload_path.mkdir(parents=True, exist_ok=True)
    return str(upload_path)


async def save_file(file: UploadFile, custom_path: str = None) -> tuple:
    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File content is empty")

    sanitized_filename = sanitize_filename(file.filename)

    if custom_path is None:
        upload_dir = Path(settings.media_path) / get_default_upload_directory(file, settings.media_path)
    else:
        upload_dir = Path(settings.media_path) / custom_path.lstrip("/") 
    
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / sanitized_filename
    
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return str(file_path), len(content)