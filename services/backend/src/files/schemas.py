from pydantic import BaseModel


class FileResponse(BaseModel):
    id: str
    name: str
    created_at: str
    path: str
    size: int
    is_downloadable: bool

    class Config:
        from_attributes = True