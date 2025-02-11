from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from models.enums import VisibilityEnum


class URLCreateRequest(BaseModel):
    original_url: str = "http://example.com"
    visibility: VisibilityEnum = VisibilityEnum.public
    
class URLCreateResponse(BaseModel):
    short_url_id: str
    short_url: str
    
class URLAccessResponse(BaseModel):
    accessed_at: datetime
    client_info: Optional[str] = None

class URLStatusResponse(BaseModel):
    short_url: str
    total_accesses: int
    accesses: List[URLAccessResponse]
    
class URLStatusRequest(BaseModel):
    full_info: bool = False
    max_result: int = 10
    offset: int = 0
    
    class Config:
        use_enum_values = True

class URLDeleteResponse(BaseModel):
    status: str
    message: str
    
class URLBatchCreateRequest(BaseModel):
    original_urls: List[URLCreateRequest]

class URLBatchCreateResponse(BaseModel):
    short_urls: List[URLCreateResponse]