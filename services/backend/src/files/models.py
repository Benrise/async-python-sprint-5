import uuid

from sqlalchemy import Column, String, Integer, Boolean, DateTime, text
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID

from .utils import sanitize_filename
from ..models import Base


class File(Base):
    __tablename__ = 'files'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    is_downloadable = Column(Boolean, default=True)

    @validates('name')
    def validate_name(self, _, value):
        sanitized = sanitize_filename(value)
        return sanitized