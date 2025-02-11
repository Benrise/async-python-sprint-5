import os

from uuid import UUID
from typing import List
from fastapi import APIRouter, File, UploadFile, Depends, APIRouter, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .models import File as FileModel
from .schemas import FileResponse
from .utils import save_file
from db.postgres import get_async_session

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), path: str = None, db: Session = Depends(get_async_session)):
    file_path, size = await save_file(file, path)

    new_file = FileModel(
        name=file.filename,
        path=file_path,
        size=size,
        is_downloadable=True
    )
    
    db.add(new_file)
    
    await db.commit()
    await db.refresh(new_file)

    return FileResponse(
        id=str(new_file.id),
        name=new_file.name,
        created_at=str(new_file.created_at),
        path=new_file.path,
        size=new_file.size,
        is_downloadable=new_file.is_downloadable
    )


@router.get("/download")
async def download_file(path: str = None, file_id: str = None, db: Session = Depends(get_async_session)):
    if not path and not file_id:
        raise HTTPException(status_code=400, detail="Either 'path' or 'file_id' must be provided")

    file = None

    if file_id:
        result = await db.execute(select(FileModel).filter(FileModel.id == UUID(file_id)))
        file = result.scalars().first()

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = file.path
    elif path:
        file_path = path
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found on server")
        
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    print(f"Sending file: {file_path}")
    
    return FastAPIFileResponse(
        path=file_path,
        filename=file.name if file else os.path.basename(file_path),
        media_type="application/octet-stream",
    )
    
    
@router.get("/", response_model=List[FileResponse])
async def get_all_files(db: Session = Depends(get_async_session)):
    files_result = await db.execute(select(FileModel))
    files = files_result.scalars().all()

    return [
        FileResponse(
            id=str(file.id),
            name=file.name,
            created_at=file.created_at.isoformat(),
            path=file.path,
            size=file.size,
            is_downloadable=file.is_downloadable
        )
        for file in files
    ]