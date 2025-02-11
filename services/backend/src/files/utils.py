import re

from pathlib import Path
from fastapi import UploadFile


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    sanitized = sanitized.replace(" ", "_")
    return sanitized

def get_upload_directory(file: UploadFile, base_path: str) -> str:
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


async def save_file(file: UploadFile, base_path: str) -> str:
    sanitized_filename = sanitize_filename(file.filename)
    upload_dir = get_upload_directory(file, base_path)
    
    path = Path(upload_dir) / sanitized_filename
    
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return str(path)
