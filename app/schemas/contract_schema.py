from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ContractBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    nature: Optional[str] = None
    project: Optional[str] = None
    path: Optional[str] = None
    created_at: Optional[datetime] = None

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: int

    class Config:
        orm_mode = True

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int

class ContractListResponse(BaseModel):
    data: list[Contract]
    meta: PaginationMeta

class ContractSearchParams(BaseModel):
    search: Optional[str] = None
    name: Optional[str] = None
    nature: Optional[str] = None
    project: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)