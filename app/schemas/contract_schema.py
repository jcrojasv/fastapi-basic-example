from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class ContractBase(BaseModel):
    name: str
    nature: str
    project: str
    path: Optional[str] = None
    created_at: Optional[datetime] = None

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int

class ContractListResponse(BaseModel):
    data: List[ContractResponse]
    meta: PaginationMeta

class ContractSearchParams(BaseModel):
    search: Optional[str] = None
    name: Optional[str] = None
    nature: Optional[str] = None
    project: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)