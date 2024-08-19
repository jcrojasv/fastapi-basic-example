from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import contract_schema
from repositories import contract_repository as repository
from config import database

router = APIRouter()


@router.get("/contracts/", response_model=contract_schema.ContractListResponse)
def get_contracts(
    params: contract_schema.ContractSearchParams = Depends(),
    db: Session = Depends(database.get_db),
):
    repo = repository.ContractRepository(db)
    contracts, total = repo.get_contracts(params)

    return {
        "data": contracts,
        "meta": {
            "page": params.page,
            "page_size": params.page_size,
            "total": total,
            "total_pages": (total + params.page_size - 1) // params.page_size,
        }
    }