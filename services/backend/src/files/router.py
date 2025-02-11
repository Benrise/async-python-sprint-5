import os
import asyncio

from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, Depends, APIRouter, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .models import File as FileModel
from .schemas import FileResponse
from .utils import save_file
from ..config import settings
from db.postgres import get_async_session

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), to_aws: bool = False, db: Session = Depends(get_async_session)):
    path = file.filename
    content = await file.read()

    new_file = FileModel(
        name=file.filename,
        path=path,
        size=len(content),
        is_downloadable=True
    )
    
    db.add(new_file)
    
    await db.commit()
    await db.refresh(new_file)
    
    if to_aws:
        # TODO: Реализовать логику загрузки в AWS
        pass
    else:
        path = await save_file(file, settings.media_path)

    return FileResponse(
        id=str(new_file.id),
        name=new_file.name,
        created_at=str(new_file.created_at),
        path=new_file.path,
        size=new_file.size,
        is_downloadable=new_file.is_downloadable
    )


@router.get("/download", response_model=FileResponse)
async def download_file(path: Optional[str] = None, file_id: Optional[str] = None, db: Session = Depends(get_async_session)):
    if not path and not file_id:
        raise HTTPException(status_code=400, detail="Provide either file path or file ID")

    if file_id:
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
    else:
        file = db.query(File).filter(File.path == path).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

    if os.path.exists(file.path):
        return FileResponse(
            id=file.id,
            name=file.name,
            created_at=file.created_at.isoformat(),
            path=file.path,
            size=file.size,
            is_downloadable=file.is_downloadable
        )
    else:
        raise HTTPException(status_code=404, detail="File not found on server")
    
    
@router.get("/", response_model=List[FileResponse])
async def get_all_files(db: Session = Depends(get_async_session)):
    files_result = await db.execute(select(FileModel))
    files = files_result.scalars().all()

    return [
        FileResponse(
            id=file.id,
            name=file.name,
            created_at=file.created_at.isoformat(),
            path=file.path,
            size=file.size,
            is_downloadable=file.is_downloadable
        )
        for file in files
    ]