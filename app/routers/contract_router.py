from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
import logging
from services.contract_service import ContractService
from sqlalchemy.orm import Session
from schemas.contract_schema import ContractCreate, ContractResponse, ContractSearchParams, ContractListResponse
from config import database

router = APIRouter()
logger = logging.getLogger(__name__)

def get_contract_service(db: Session):
    return ContractService(db)

def handle_exception(e: Exception, message: str, status_code: int = 400):
    logger.error(message, exc_info=True)
    raise HTTPException(status_code=status_code, detail=f"{message}. {str(e)}")

@router.get("/contracts/", response_model=ContractListResponse)
def get_contracts(
    params: ContractSearchParams = Depends(),
    db: Session = Depends(database.get_db),
):
    try:
        service = get_contract_service(db)
        contracts, total = service.get_contracts(params)
        return {
            "data": contracts,
            "meta": {
                "page": params.page,
                "page_size": params.page_size,
                "total": total,
                "total_pages": (total + params.page_size - 1) // params.page_size,
            }
        }
    except Exception as e:
        handle_exception(e, "An error occurred while fetching contracts")

@router.post("/contracts/", response_model=ContractResponse)
async def create_contract(
    name: str = Form(...),
    nature: str = Form(...),
    project: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    try:
        logger.info(f"Received request to create contract: name={name}, nature={nature}, project={project}")

        if file is None:
            raise HTTPException(status_code=400, detail="File is required.")

        contract_data = ContractCreate(name=name, nature=nature, project=project)
        service = get_contract_service(db)
        contract = service.create_contract_with_file(contract_data, file)
        logger.info(f"Contract created successfully with ID: {contract.id}")
        return contract
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_exception(e, "An error occurred while creating the contract")

@router.get("/contracts/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(database.get_db),
):
    try:
        service = get_contract_service(db)
        contract = service.get_contract_by_id(contract_id)

        if contract is None:
            raise HTTPException(status_code=404, detail="Contract not found.")

        return contract
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_exception(e, f"An error occurred while fetching contract with ID {contract_id}")

@router.delete("/contracts/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(database.get_db),
):
    try:
        service = get_contract_service(db)
        deleted = service.delete_contract(contract_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Contract not found.")

        return {"message": "Contract deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_exception(e, f"An error occurred while deleting contract with ID {contract_id}")