from pydantic import BaseModel
from typing import Optional

class ContractBase(BaseModel):
    name: Optional[str] = None
    nature: Optional[str] = None
    project: Optional[str] = None

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