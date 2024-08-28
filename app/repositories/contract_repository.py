
import logging
from sqlalchemy import or_
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models import contract_model
from contextlib import contextmanager
from schemas.contract_schema import ContractSearchParams

logger = logging.getLogger(__name__)

@contextmanager
def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


class ContractRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contracts(self, params: ContractSearchParams):
        try:
            query = self.db.query(contract_model.Contract)

            if params.search:
                search_term = f"%{params.search}%"
                query = query.filter(
                    contract_model.Contract.name.like(search_term) |
                    contract_model.Contract.nature.like(search_term) |
                    contract_model.Contract.project.like(search_term)
                )

            if params.name:
                query = query.filter(contract_model.Contract.name.like(f"%{params.name}%"))
            if params.nature:
                nature_filters = params.nature.split("|")
                query = query.filter(or_(*[contract_model.Contract.nature.like(f"%{n}%") for n in nature_filters]))
            if params.project:
                project_filters = params.project.split("|")
                query = query.filter(or_(*[contract_model.Contract.project.like(f"%{p}%") for p in project_filters]))

            total = query.count()
            contracts = query.offset((params.page - 1) * params.page_size).limit(params.page_size).all()

            return contracts, total
        except Exception as e:
            logger.error(f"Error getting contracts: {e}")
            raise

    def create_contract(self, contract: contract_model.Contract):
        try:
            logger.info(f"[ContractRepository] Creating contract: {contract}")
            self.db.add(contract)
            self.db.commit()
            self.db.refresh(contract)
            logger.info(f"[ContractRepository] Contract created successfully: {contract.id}")
            return contract
        except Exception as e:
            logger.error(f"Error creating contract: {e}")
            self.db.rollback()
            raise

    def get_contract_by_id(self, contract_id: int):
        try:
            return self.db.query(contract_model.Contract).filter(contract_model.Contract.id == contract_id).first()
        except Exception as e:
            logger.error(f"Error getting contract by id {contract_id}: {e}")
            raise

    def delete_contract(self, contract_id: int):
        try:
            contract = self.get_contract_by_id(contract_id)
            if contract:
                self.db.delete(contract)
                self.db.commit()
                logger.info(f"[ContractRepository] Contract deleted successfully: {contract_id}")
                return True
            else:
                logger.warning(f"[ContractRepository] Contract not found: {contract_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting contract by id {contract_id}: {e}")
            self.db.rollback()
            raise