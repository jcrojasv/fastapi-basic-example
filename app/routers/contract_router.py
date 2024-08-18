from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas import contract_schema
from repositories import contract_repository as repository
from config import database

router = APIRouter()


@router.get("/contracts/", response_model=contract_schema.ContractListResponse)
def get_contracts(
    name: str = Query(None),
    nature: str = Query(None),
    project: str = Query(None),
    page: int = Query(1),
    page_size: int = Query(10),
    db: Session = Depends(database.get_db),
):
    repo = repository.ContractRepository(db)
    contracts, total = repo.get_contracts(
        name=name,
        nature=nature,
        project=project,
        page=page,
        page_size=page_size
    )

    return {
        "data": contracts,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
        }
    }